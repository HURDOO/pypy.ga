import json

from . import grader
from submit.models import Submit, SubmitType, ResultType


def handle_data(container, submit_id: int, problem_id:int, submit_type: SubmitType):

    # docker.transport.npipesocket.NpipeSocket
    # similar to python socket
    socket = container.attach_socket()

    while True:
        end = False

        _ = socket.recv(8)  # unused bytes

        input_ongoing = False
        input_string = ''
        case_idx_ongoing = -1
        not_found_cnt = 0

        for s in socket.recv(16384).decode().split('\n'):
            print(s)

            try:
                data = json.loads(s)
            except json.JSONDecodeError as err:

                if input_ongoing:
                    input_string += s + '\n'
                    continue
                else:
                    print(input_ongoing)
                    print(s)
                    raise err

            if data['type'] in ['START', 'PREPARE', 'FOUND']:
                pass

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
                        # TODO Judge
                        if not grader.handle_data(input_string, problem_id, case_idx_ongoing):
                            print('failed', case_idx_ongoing)
                            submit = Submit.objects.get(id=submit_id)
                            submit.end(
                                _result=ResultType.WRONG_ANSWER,
                                _time_usage=0,
                                _memory_usage=0,
                                _stdout=input_string,
                                _stderr=None
                            )
                            end = True
                            break
                        else:
                            print('passed', case_idx_ongoing)
                        pass
                    else:
                        # TODO save output
                        pass

                elif data['result'] == 'TLE':
                    # TODO Time Limit Error
                    pass

                elif data['result'] == 'RTE':
                    # TODO RunTime Error
                    pass

                else:
                    print('unknown case_end')
                    print(data)
                    break
                case_idx_ongoing = -1
                input_ongoing = False
                input_string = ''

            elif data['type'] == 'END':
                # TODO send result
                end = True
                break

            else:
                print('unknown type')
                print(data)

        if end:
            break
    print("end")
