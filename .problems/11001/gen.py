def get_input_output() -> list[tuple[str,str]]:
    lst = []

    for i in range(100, -1, -1):
        if i >= 60:
            res = '합격입니다.'
        else:
            res = '불합격입니다.'
        res += '\n수고하셨습니다.'

        lst.append((str(i), res))

    return lst
