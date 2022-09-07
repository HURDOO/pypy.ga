import os
from pathlib import Path

import docker
import tarfile
from pypyga.settings import BASE_DIR
from multiprocessing import Process, Queue
from submit.models import Submit, SubmitType
from . import result
from problem.load import PROBLEMS_DIR

DOCKER_IMAGE_NAME = 'test1234'
DOCKER_NAME = 'runner_{}'
TEMP_DIR = BASE_DIR / '.tmp'
SUB_RUNNER_NAME = 'sub_runner.py'

PROCESS_LIMIT = 10
proc_cnt = 0
proc_waiting = Queue()


def run_docker(submit_id: int, case_cnt: int):
    client = docker.from_env()
    # client.containers.prune()

    return client.containers.run(
        image=DOCKER_IMAGE_NAME,
        command=['python', SUB_RUNNER_NAME, str(case_cnt)],
        name=DOCKER_NAME.format(submit_id),
        detach=True,
        network_disabled=True,
    )


def send_data(container, submit_id: int, work_dir: Path):
    with open(work_dir / '{}.tar'.format(submit_id), 'rb') as tar:
        container.put_archive('~/docker_dir/', tar)


def handle_submit(
        submit_id: int,
        problem_id: int,
        code: str,
        submit_type: SubmitType,
        input_data: str = None
):
    try:
        work_dir = TEMP_DIR / str(submit_id)
        os.mkdir(work_dir)

        case_cnt = create_tar(submit_id, problem_id, code, submit_type, work_dir, input_data)
        container = run_docker(submit_id, case_cnt)

        socket = container.attach_socket()
        send_data(container, submit_id, work_dir)
        result.handle_data(socket, submit_id, problem_id, submit_type)
        container.stop()
        container.remove()
    except Exception as err:
        Submit.objects.get(id=submit_id).internal_error(_stderr=str(err))


def create_tar(
        submit_id: int,
        problem_id: int,
        code: str,
        submit_type: SubmitType,
        work_dir: Path,
        input_data: str = None
) -> int:
    cnt = 0

    # save code
    code_file_name = 'code.py'
    with open(work_dir / code_file_name, 'w', encoding='UTF-8') as code_file:
        code_file.write(code)
        code_file.close()

    # make tar file
    tarfile_name = '{}.tar'.format(submit_id)
    with tarfile.open(work_dir / tarfile_name, 'w', encoding='UTF-8') as tar:
        tar.add(work_dir / code_file_name, arcname=code_file_name)

        # copy grading input
        if submit_type == SubmitType.GRADE:
            case_dir = PROBLEMS_DIR / str(problem_id) / 'in'
            for root, dirs, files in os.walk(case_dir):
                for filename in files:
                    tar.add(case_dir / filename, arcname=filename)
                    cnt += 1

        # save custom input
        else:
            input_file_name = '1.in'
            with open(work_dir / input_file_name, 'w', encoding='UTF-8') as input_file:
                if input_data is not None:
                    input_file.write(input_data)
                input_file.close()
            tar.add(work_dir / input_file_name, arcname=input_file_name)
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
