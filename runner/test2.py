import docker


def test():
    client = docker.from_env()
    name = 'test1234'

    client.containers.prune()

    container = client.containers.run(
        image="ubuntu",
        command=[
            'sh',
            '-c',
            'echo 1 && echo 2'
        ],
        name=name
    )
    print(container)
