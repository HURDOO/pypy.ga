def get_input_output() -> list[tuple[str, str]]:
    lst = [('강호\n강호', "'강호'\n\"강호\"")]
    for s in '박유민, 배철희, 홍기준, 사공윤주, 노연재, 류윤태, 임시원, 탁경선, 백서은, 심명숙' \
             ', 복시정, 김경호, 김재웅, 사공명원, 예원빈, 장문용, 사공석호, 안정우, 복소미, 김시아'.split(', '):
        lst.append((f"{s}\n{s}", "'{}'\n\"{}\"".format(s, s)))
    return lst
