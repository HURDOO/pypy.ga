def get_input_output() -> list[tuple[str, str]]:
    lst = []

    for s in ['ㅇㅅㅇ', 'ㅎㅅㅎ', 'ㅇㅁㅇ', 'ㅇ_ㅇ', 'ㅁㅅㅁ', 'ㅋㅅㅋ', 'ㅡㅅㅡ', 'ㅎㅅㅎ', 'ㅠㅛㅠ',
              'ㅇ3ㅇ', 'ㅇwㅇ', 'ㅇㅂㅇ', 'ㅇㅈㅇ', 'ㅇㅠㅇ', 'ㅎㅁㅎ']:
        lst.append((s, str(s.count('ㅇ'))))

    return lst
