def get_input_output() -> list[tuple[str, str]]:
    ans = ''
    for i in range(5):
        for j in range(10):
            ans += '* '
        ans += '\n'
    return [('', ans)]
