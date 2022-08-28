# import resource
from subprocess import Popen, PIPE
from multiprocessing import Pool


def run(file_path: str):
    process = Popen(
        ['python', file_path],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        bufsize=10000,
        # preexec_fn=limit
    )

    out, err = process.communicate(
        input='asdf'.encode(),
        timeout=2,
    )
    if err == b'':
        print(out.decode(), end='')
    else:
        print(err.decode())


MAX_MEMORY = 128 * 1024 * 1024


def limit():
    # resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
    pass


if __name__ == '__main__':
    for _ in range(10):
        run("print('Hello World!')")
