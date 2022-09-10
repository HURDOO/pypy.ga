from subprocess import Popen, PIPE, TimeoutExpired
from multiprocessing import Process, Value
import sys
import os
import time
import json
import psutil
import resource

TIME_LIMIT = 5  # 5s
MEMORY_LIMIT = 128 * 1024 * 1024  # 128MB


def output(data: dict):
    print(json.dumps(data))


def run(code_file: str, case_num: int):
    output({'type': 'PREPARE'})

    while True:
        if os.path.exists(code_file):
            output({'type': 'FOUND'})
            break
        output({'type': 'NOT_FOUND'})
        time.sleep(0.5)

    for i in range(1, case_num + 1):

        output({
            'type': 'CASE_START',
            'case_idx': i,
        })

        proc = Popen(
            ['python', code_file],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            bufsize=10000,
            preexec_fn=limit_mem
        )

        mem = Value('i', 0)
        mem_proc = Process(target=mem_check, args=(proc.pid, mem), daemon=True)
        try:
            with open('{}.in'.format(i)) as f:
                before = time.time()
                mem_proc.start()

                out, err = proc.communicate(
                    input=f.read().encode(),
                    timeout=TIME_LIMIT,
                )

                after = time.time()
                mem_proc.terminate()

                if err == b'':
                    # print(out.decode(), end='')
                    output({
                        'type': 'CASE_END',
                        'result': 'END',
                        'case_idx': i,
                        'time': after - before,
                        'memory': mem.value,
                        'out': out.decode()
                    })
                else:
                    # print(out.decode(), end='')
                    output({
                        'type': 'CASE_END',
                        'result': 'RTE',
                        'case_idx': i,
                        'time': after - before,
                        'memory': mem.value,
                        'out': out.decode(),
                        'err': err.decode()
                    })
                    # print(err.decode(), end='')
                    break

        except TimeoutExpired:
            output({
                'type': 'CASE_END',
                'result': 'TLE',
                "case_idx": i
            })
            break

    output({
        'type': 'END',
        'result': 'END'
    })


def limit_mem():
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
    pass


def mem_check(pid: int, mem: Value) -> None:
    proc = psutil.Process(pid)
    while True:
        memory_usage = proc.memory_info().rss
        if memory_usage > mem.value:
            mem.value = memory_usage


if __name__ == '__main__':
    output({'type': 'START'})
    _, _case_num = sys.argv
    run("code.py", int(_case_num))
