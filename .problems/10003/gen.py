def get_input_output() -> list[tuple[str, str]]:
    lst = []
    for s in '유은미, 황광희, 정희선, 봉인태, 예미영, 설현빈, 문남혁, 이현빈, 황은경, 강연진' \
            ', 문민웅, 홍영우, 권선희, 제갈문철, 류명진, 문시우, 봉설현, 김다연, 복용남, 남궁지희'.split(', '):
        lst.append((s, s))
    return lst
