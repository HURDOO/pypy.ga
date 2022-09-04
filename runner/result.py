import json
import platform

from . import grader
from submit.models import Submit, SubmitType, ResultType


def handle_data(container, submit_id: int, problem_id: int, submit_type: SubmitType):
    # docker.transport.npipesocket.NpipeSocket
    # similar to python socket
    socket = container.attach_socket()

    input_ongoing = False
    input_string = ''
    case_idx_ongoing = -1
    not_found_cnt = 0

    submit = Submit.objects.get(id=submit_id)
    result = ResultType.PREPARE
    memory_usage = 0
    time_usage = 0
    stdout = None
    stderr = None

    while True:
        end = False

        if platform.system() == 'Windows':
            response = socket.recv(1024 * 1024)
        else:
            response = socket.read()

        while b'\x01' in response:
            index = response.index(b'\x01')
            tmp = bytes()
            if index > 0:
                tmp = response[:index-1]
            tmp += '\n'.encode()
            tmp += response[index+8:]
            response = tmp

        # for s in socket.recv(16384).decode().split('\n'):
        for s in response.decode(encoding='utf-8').split('\n'):
            if len(s) == 0:
                continue
            print(s)
            try:
                data = json.loads(s)
                _ = data['type']
            except (json.JSONDecodeError, TypeError) as err:

                if input_ongoing:
                    input_string += s + '\n'
                    continue
                else:
                    print(s)
                    raise Exception([
                        ValueError(s),
                        err
                    ])

            if data['type'] in ['START', 'PREPARE']:
                pass

            elif data['type'] == 'FOUND':
                result = ResultType.ONGOING

            elif data['type'] == 'NOT_FOUND':
                not_found_cnt += 1
                if not_found_cnt >= 10:
                    # TODO Internal Error
                    break

            elif data['type'] == 'CASE_START':
                case_idx_ongoing = data['case_idx']
                input_ongoing = True
                input_string = ''

            elif data['type'] == 'CASE_END':
                if data['result'] == 'END':
                    if submit_type == SubmitType.GRADE:
                        if not grader.handle_data(input_string, problem_id, case_idx_ongoing):
                            print('failed', case_idx_ongoing)
                            result, stdout, stderr \
                                = ResultType.WRONG_ANSWER, input_string, None
                            end = True
                            break
                        else:
                            if data['time'] > time_usage:
                                time_usage = int(data['time'] * 1000)  # ms
                            if data['memory'] > memory_usage:
                                memory_usage = int(data['memory'] / 1024)  # kb
                            print('passed', case_idx_ongoing)

                        pass
                    else:
                        result, time_usage, memory_usage, stdout \
                            = ResultType.COMPLETE, data['time'], data['memory'], input_string
                        end = True
                        break

                elif data['result'] == 'TLE':
                    result = ResultType.TIME_LIMIT
                    end = True
                    break

                elif data['result'] == 'RTE':
                    # TODO stderr
                    result, stderr = ResultType.RUNTIME_ERROR, input_string
                    end = True
                    break

                else:
                    print('unknown case_end')
                    print(data)
                    break

                case_idx_ongoing = -1
                print('input_ongoing changed to false')
                input_ongoing = False
                input_string = ''

            elif data['type'] == 'END':
                end = True
                break

            else:
                print('unknown type')
                print(data)

        if end:
            if result == ResultType.ONGOING:
                result = ResultType.ACCEPTED
            submit.end(
                _result=result,
                _time_usage=time_usage,
                _memory_usage=memory_usage,
                _stdout=stdout,
                _stderr=stderr
            )
            break
    print("end")
