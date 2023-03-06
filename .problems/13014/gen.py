def get_input_output() -> list[tuple[str, str]]:
    lst = []

    arr = ['1', '1']
    for i in range(3, 21):  # 4 ~ 20
        arr.append(str(int(arr[i-2]) + int(arr[i-3])))  # 0 base
        lst.append((str(i), "\n".join(arr)))

    lst.extend([("1", "1"), ("2", "1\n1")])

    return lst
