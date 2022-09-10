import json
import platform
import re

from . import grader
from submit.models import Submit, SubmitType, ResultType


def handle_data(socket, submit_id: int, problem_id: int, submit_type: SubmitType, case_cnt: int) -> None:
    # docker.transport.npipesocket.NpipeSocket
    # similar to python socket
    # https://docs.docker.com/engine/api/v1.24/#attach-to-a-container

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

        if platform.system() == 'Windows':  # NpipeSocket
            response = socket.recv(1024 * 1024 * 128)  # 128MB
        else:  # SocketIO
            response = socket.read()

        if len(response) == 0:
            continue

        # print(response.hex())

        base = 0
        while base < len(response):
            size = 0

            if response[base] == 1:  # stdout
                for i in range(4, 8):
                    size <<= 8
                    size += response[base + i]

            else:  # stdin, stderr, or something else
                raise Exception(response.hex())

            decoded = response[base + 8:base + 8 + size].decode(encoding='utf-8').splitlines()
            # responses.extend(decoded)
            base += size + 8

            for s in decoded:

                if len(s) == 0:
                    continue
                # print(s)

                try:
                    data = json.loads(s)
                    _ = data['type']
                except (json.JSONDecodeError, TypeError) as err:
                    raise err

                if data['type'] in ['START', 'PREPARE']:
                    pass

                elif data['type'] == 'FOUND':
                    result = ResultType.ONGOING
                    submit.start()

                elif data['type'] == 'NOT_FOUND':
                    not_found_cnt += 1
                    if not_found_cnt >= 10:
                        raise Exception('NOT_FOUND')

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
                                submit.case_done(case_idx_ongoing / case_cnt * 100)
                                # print('passed', case_idx_ongoing)

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
                        err = parse_error(data['err'])
                        if 'stderr' not in err and err['error'] == 'MemoryError\n':
                            result, stdout, stderr \
                                = ResultType.MEMORY_LIMIT, data['out'], err
                        else:
                            result, stdout, stderr \
                                = ResultType.RUNTIME_ERROR, data['out'], err
                        end = True
                        break

                    else:
                        raise Exception('unknown case_end result: ' + str(data['result']))

                    case_idx_ongoing = -1

                elif data['type'] == 'END':
                    end = True
                    break

                else:
                    raise Exception('unknown type: ' + str(data['type']))
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
        # socket not closed
        if end:
            break
    print("end")


"""
    Group 1: line number
    Group 2: line code
    Group 3: error name
    Group 4: error cause
"""
err_re = re.compile(
    r'^Traceback \(most recent call last\):\n'
    '  File "/~/docker_dir/code.py", line (\\d+), in <module>\n'
    '    ([^\n]+)\n'
    '([^:]+):? ?([^\n]+)?')


def parse_error(stderr: str) -> dict:

    # TODO: SyntaxError handling

    match = err_re.match(stderr)
    if match is None:
        return {
            'stderr': stderr
        }

    data = {
        'line_num': int(match.group(1))//2+1,
        'line_code': match.group(2),
        'error': match.group(3)
    }
    try:
        data['cause'] = match.group(4)
    except AttributeError:
        data['cause'] = 'None'

    return data
