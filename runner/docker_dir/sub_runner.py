# import resource
import ctypes
from subprocess import Popen, PIPE, TimeoutExpired
from multiprocessing import Process, Value, sharedctypes
import sys
import os
import time
import json
import psutil


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
            # preexec_fn=limit
        )

        mem = Value('i', 0)
        # TODO look for alternative of Value
        mem_proc = Process(target=mem_check, args=(proc.pid, mem), daemon=True)
        try:
            with open('{}.in'.format(i)) as f:
                before = time.time()
                mem_proc.start()

                out, err = proc.communicate(
                    input=f.read().encode(),
                    timeout=5,
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


MAX_MEMORY = 128 * 1024 * 1024


# def limit():
#     # resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
#     pass


def mem_check(pid: int, mem: Value) -> None:
    proc = psutil.Process(pid)
    while True:
        try:
            memory_usage = proc.memory_info().rss
            if memory_usage > mem.value:
                mem.value = memory_usage
        except psutil.NoSuchProcess:
            print('cannot find process')
            pass


if __name__ == '__main__':
    output({'type': 'START'})
    _, _case_num = sys.argv
    run("code.py", int(_case_num))
