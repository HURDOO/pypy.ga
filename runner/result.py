import json
import platform

from . import grader
from submit.models import Submit, SubmitType, ResultType


def handle_data(socket, submit_id: int, problem_id: int, submit_type: SubmitType):
    # docker.transport.npipesocket.NpipeSocket
    # similar to python socket

    case_idx_ongoing = -1
    not_found_cnt = 0

    submit = Submit.objects.get(id=submit_id)
    result = ResultType.PREPARE
    memory_usage = 0
    time_usage = 0
    stdout = None
    stderr = None

    responses = []

    while True:
        end = False

        if platform.system() == 'Windows':
            response = socket.recv(1024 * 1024)
        else:
            response = socket.read()

        if b'\x02' in response:
            print('error detected')

        while b'\x01' in response:
            index = response.index(b'\x01')
            tmp = bytes()
            if index > 0:
                tmp = response[:index-1]
            tmp += '\n'.encode()
            tmp += response[index+8:]
            response = tmp

        decoded = response.decode(encoding='utf-8').split('\n')
        responses.extend(decoded)

        # for s in socket.recv(16384).decode().split('\n'):
        for s in decoded:
            if len(s) == 0:
                continue
            print(s)
            try:
                data = json.loads(s)
                _ = data['type']
            except (json.JSONDecodeError, TypeError) as err:
                print(s)
                raise err

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

            elif data['type'] == 'CASE_END':
                if data['case_idx'] != case_idx_ongoing:
                    raise Exception('case_idx not equals to case_idx_ongoing')

                if data['result'] == 'END':

                    if submit_type == SubmitType.GRADE:

                        if not grader.handle_data(data['out'], problem_id, case_idx_ongoing):
                            print('failed', case_idx_ongoing)
                            result, stdout, stderr \
                                = ResultType.WRONG_ANSWER, data['out'], None
                            end = True
                            break

                        else:
                            if data['time'] > time_usage:
                                time_usage = int(data['time'] * 1000)  # ms
                            if data['memory'] > memory_usage:
                                memory_usage = int(data['memory'] / 1024)  # kb
                            print('passed', case_idx_ongoing)

                    else:
                        result, time_usage, memory_usage, stdout \
                            = ResultType.COMPLETE, data['time'], data['memory'], data['out']
                        end = True
                        break

                elif data['result'] == 'TLE':
                    result = ResultType.TIME_LIMIT
                    end = True
                    break

                elif data['result'] == 'RTE':
                    result, stdout, stderr \
                        = ResultType.RUNTIME_ERROR, data['out'], data['err']
                    end = True
                    break

                else:
                    print('unknown case_end')
                    print(data)
                    break

                case_idx_ongoing = -1

            elif data['type'] == 'END':
                end = True
                break

            else:
                print('unknown type')
                print(data)

        if end:
            if result == ResultType.ONGOING:
                result = ResultType.ACCEPTED
            if case_idx_ongoing == -1:
                case_idx_ongoing = None
            submit.end(
                _result=result,
                _time_usage=time_usage,
                _memory_usage=memory_usage,
                _stdout=stdout,
                _stderr=stderr,
                _last_case_idx=case_idx_ongoing
            )
            break
    print("end")
