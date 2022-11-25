def get_input_output() -> list[tuple[str, str]]:
    ans = ''
    for i in range(1, 6):
        for j in range(1, i+1):
            ans += '* '
        ans += '\n'
    return [('', ans)]
