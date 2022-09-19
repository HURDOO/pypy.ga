def get_input_output() -> list[tuple[str, str]]:
    lst = []

    for a in ['짜장면', '짬뽕']:
        for b in ['신라면', '진라면']:
            for c in ['물냉면', '비빔냉면']:
                for d in ['파스타', '스파게티']:
                    lst.append((f'{a}\n{b}\n{c}\n{d}', f'{a}하고 {b}하고 {c}하고 {d}'))

    return lst
