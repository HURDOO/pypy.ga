import random
import string


def get_input_output() -> list[tuple[str, str]]:
    lst = [("rodela\nrodela", "비밀번호가 변경되었습니다"), ("rodela\nrodlea", "비밀번호를 다시 확인해주세요")]
    random.seed(13010)

    for _ in range(10):
        pw = ""
        for __ in range(random.randint(4, 10)):
            pw += ''.join(random.sample(string.ascii_lowercase + string.digits, k=1))
        if random.randint(1, 2) == 1:
            check = pw
            output = "비밀번호가 변경되었습니다"
        else:
            check = ''.join(random.sample(pw, len(pw)))
            output = "비밀번호를 다시 확인해주세요"

        lst.append((f'{pw}\n{check}', output))

    return lst
