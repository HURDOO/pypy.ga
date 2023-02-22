def get_input_output() -> list[tuple[str, str]]:
    ans = ''
    sum = 0

    for i in range(1, 11):
        sum += i
        if i % 2 == 0:
            ans += '1부터 {}까지의 합은 {}입니다.\n' .format(i, sum)

    return [('', ans)]
