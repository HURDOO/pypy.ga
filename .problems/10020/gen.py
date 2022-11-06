def get_input_output() -> list[tuple[str,str]]:
    output = ''
    for i in range(1, 151):
        output += f'{i}\n'
    return [('', output)]
