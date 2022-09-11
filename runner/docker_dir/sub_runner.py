import signal
import subprocess
from subprocess import Popen, PIPE, TimeoutExpired
from multiprocessing import Process, Value
from threading import Thread
import sys
import os
import time
import json
import psutil

# import resource

TIME_LIMIT = 5  # 5s
MEMORY_LIMIT = 128 * 1024 * 1024  # 128MB

CODE_FILE = 'code.py'


def output(data: dict):
    print(json.dumps(data))


def run(case_cnt: int):
    output({'type': 'PREPARE'})

    while True:
        if os.path.exists('output_size.json'):
            output({'type': 'FOUND'})
            break
        output({'type': 'NOT_FOUND'})
        time.sleep(0.5)

    with open('output_size.json', 'r', encoding='utf-8') as f:
        output_lens = json.loads(f.read())

    for i in range(1, case_cnt + 1):

        output({
            'type': 'CASE_START',
            'case_idx': i,
        })

        in_file = open(f'{i}.in', 'r', encoding='utf-8')
        out_file = open('case.out', 'w', encoding='utf-8')
        err_file = open('case.err', 'w', encoding='utf-8')

        proc = Popen(
            ['python', CODE_FILE],
            stdin=in_file,
            stdout=out_file,
            stderr=err_file,
            # preexec_fn=limit_mem
        )

        mem = Value('i', 0)
        mem_proc = Process(target=mem_check, args=(proc.pid, mem), daemon=True)

        before = time.time()
        mem_proc.start()  # run() -> delay X

        try:
            proc.wait(
                timeout=TIME_LIMIT
            )

        except TimeoutExpired:
            output({
                'type': 'CASE_END',
                'result': 'TLE',
                "case_idx": i
            })
            break

        finally:
            proc.kill()

        after = time.time()
        mem_proc.terminate()

        out_file.close()
        err_file.close()

        out_file = open('case.out', 'r', encoding='utf-8')
        err_file = open('case.err', 'r', encoding='utf-8')

        if os.stat(out_file.name).st_size > output_lens[i - 1] * 2:
            output({
                'type': 'CASE_END',
                'result': 'OLE',
                'case_idx': i
            })
            break

        if os.stat(err_file.name).st_size <= 3:
            # no error
            output({
                'type': 'CASE_END',
                'result': 'END',
                'case_idx': i,
                'time': after - before,
                'memory': mem.value,
                'out': out_file.read()
            })
        else:
            # runtime error & memory error
            output({
                'type': 'CASE_END',
                'result': 'RTE',
                'case_idx': i,
                'out': out_file.read(),
                'err': err_file.read()
            })
            break

    output({
        'type': 'END',
        'result': 'END'
    })


def limit_mem():
    # resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
    pass


def mem_check(pid: int, mem: Value) -> None:
    proc = psutil.Process(pid)
    try:
        while True:
            memory_usage = proc.memory_info().rss
            if memory_usage > mem.value:
                mem.value = memory_usage
    except psutil.NoSuchProcess:
        pass


if __name__ == '__main__':
    output({'type': 'START'})
    _, _case_cnt = sys.argv
    run(int(_case_cnt))
