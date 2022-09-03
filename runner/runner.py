import os
import docker
import tarfile
from pypyga.settings import BASE_DIR
from multiprocessing import Process, Queue
from submit.models import SubmitType
import json
from . import grader
import time
from docker.types import Ulimit

DOCKER_IMAGE_NAME = 'test1234'
DOCKER_NAME = 'test1234'

PROCESS_LIMIT = 10
proc_cnt = 0
proc_waiting = Queue()


def run_docker(case_cnt: int):
    client = docker.from_env()
    client.containers.prune()

    return client.containers.run(
        image=DOCKER_IMAGE_NAME,
        command=['python', 'sub_runner.py', str(case_cnt)],
        name=DOCKER_NAME,
        detach=True,
        network_disabled=True,
    )


def send_data(container, submit_id: int):
    with open(BASE_DIR / '{}.tar'.format(submit_id), 'rb') as tar:
        container.put_archive('~/docker_dir/', tar)


def handle_submit(
        submit_id: int,
        problem_id: int,
        code: str,
        submit_type: SubmitType,
        input_data: str = None
):
    case_cnt = create_tar(submit_id, problem_id, code, submit_type, input_data)
    container = run_docker(case_cnt)
    send_data(container, submit_id)
    handle_data(container, submit_id, problem_id, submit_type)

    pass


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


def create_tar(
        submit_id: int,
        problem_id: int,
        code: str,
        submit_type: SubmitType,
        input_data: str = None
) -> int:
    cnt = 0

    code_file_name = 'code.py'
    with open(BASE_DIR / code_file_name, 'w', encoding='UTF-8') as code_file:
        code_file.write(code)
        code_file.close()

    tarfile_name = '{}.tar'.format(submit_id)
    with tarfile.open(BASE_DIR / tarfile_name, 'w', encoding='UTF-8') as tar:
        tar.add(BASE_DIR / code_file_name, arcname=code_file_name)

        if submit_type == SubmitType.GRADE:
            case_dir = BASE_DIR / 'runner' / str(problem_id)
            for root, dirs, files in os.walk(case_dir):
                for filename in files:
                    if filename.endswith('.in'):
                        tar.add(case_dir / filename, arcname=filename)
                        cnt += 1

        else:
            input_file_name = '1.in'
            with open(BASE_DIR / input_file_name, 'w', encoding='UTF-8') as input_file:
                if input_data is not None:
                    input_file.write(input_data)
                input_file.close()
            tar.add(BASE_DIR / input_file_name, arcname=input_file_name)
            cnt = 1
        tar.close()

    return cnt


def register_submit(
        submit_id: int,
        problem_id: int,
        code: str,
        submit_type: SubmitType,
        input_data: str = None
) -> None:
    # if process is full
    if proc_cnt > PROCESS_LIMIT:
        proc_waiting.put((submit_id, problem_id, code, submit_type, input_data))
        return

    proc = Process(
        target=handle_submit,
        args=(submit_id, problem_id, code, submit_type, input_data),
        daemon=True
    )
    proc.start()


def test2():
    handle_submit(5678, 10005, "print('hello world!')\r\n", SubmitType.GRADE, None)
