import json
import os
import re
import tempfile
from pathlib import Path

import docker
import tarfile
from concurrent.futures.thread import ThreadPoolExecutor
from submit.models import Submit, SubmitType
from . import result
from problem.load import PROBLEMS_DIR
import traceback

DOCKER_IMAGE_NAME = 'pypyga'
DOCKER_NAME = 'runner_{}'
SUB_RUNNER_NAME = 'sub_runner.py'

DOCKER_LIMIT = 10
executor = ThreadPoolExecutor(DOCKER_LIMIT)


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
        with tempfile.TemporaryDirectory() as work_dir:

            work_dir_path = Path(work_dir)

            case_cnt = create_tar(submit_id, problem_id, code, submit_type, work_dir_path, input_data)
            container = run_docker(submit_id, case_cnt)

            socket = container.attach_socket()
            send_data(container, submit_id, work_dir_path)

        result.handle_data(socket, submit_id, problem_id, submit_type, case_cnt)

        container.stop()
        container.remove()

    except Exception:
        Submit.objects.get(id=submit_id).internal_error(_stderr=traceback.format_exc())


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

        # delete interactive input - as it goes to stdout
        safe_code = re.sub(r'input\([\'\"](.)*[\'\"]\)', 'input()', code)

        code_file.write(safe_code)
        code_file.close()

    # make tar file
    tarfile_name = '{}.tar'.format(submit_id)
    with tarfile.open(work_dir / tarfile_name, 'w', encoding='UTF-8') as tar:
        tar.add(work_dir / code_file_name, arcname=code_file_name)
        out_lens = []

        # Grade
        if submit_type == SubmitType.GRADE:

            # copy input files
            in_dir = PROBLEMS_DIR / str(problem_id) / 'in'
            for root, dirs, files in os.walk(in_dir):
                for filename in files:
                    tar.add(in_dir / filename, arcname=filename)
                    cnt += 1

            # retrieve output file size
            out_dir = PROBLEMS_DIR / str(problem_id) / 'out'
            for i in range(1, cnt+1):
                out_lens.append(os.stat(out_dir / '{}.out'.format(i)).st_size)

        # Test
        else:
            input_file_name = '1.in'
            with open(work_dir / input_file_name, 'w',
                      encoding='UTF-8', newline='\n') as input_file:
                if input_data is not None:
                    input_file.write(input_data.replace('\r\n', '\n'))
                input_file.close()
            tar.add(work_dir / input_file_name, arcname=input_file_name)
            cnt = 1
            out_lens = [512]  # up to 1024(≒1000) characters

        # save output size
        output_file_name = 'output_size.json'
        with open(work_dir / output_file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(out_lens))
        tar.add(work_dir / output_file_name, arcname=output_file_name)

        # make empty stdout and stderr file
        with open(work_dir / 'case.out', 'w', encoding='utf-8'):
            pass
        with open(work_dir / 'case.err', 'w', encoding='utf-8'):
            pass

        tar.close()

    return cnt


def register_submit(
        submit_id: int,
        problem_id: int,
        code: str,
        submit_type: SubmitType,
        input_data: str = None
) -> None:
    # pool.apply_async(
    #     func=handle_submit,
    #     args=(submit_id, problem_id, code, submit_type, input_data)
    # )

    executor.submit(
        handle_submit,
        submit_id, problem_id, code, submit_type, input_data
    )
