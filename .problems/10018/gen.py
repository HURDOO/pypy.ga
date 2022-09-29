import random
import string


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    random.seed(10018)

    for _ in range(30):
        s = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ')
                    for _ in range(0, 100)).join(' ' for _ in range(0, 100))
        lst.append((f'{s}\n{s}', '맞았습니다!!'))

    for _ in range(30):
        s1 = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ')
                     for _ in range(0, 100)).join(' ' for _ in range(0, 100))
        s2 = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ')
                     for _ in range(0, 100)).join(' ' for _ in range(0, 100))
        lst.append((f'{s1}\n{s2}', '틀렸습니다'))

    random.shuffle(lst)

    lst.insert(0, ('나랏말싸미 듕긕에 달아     \n나랏말싸미 듕긕에 달아', '맞았습니다!!'))
    lst.insert(1, ('문짱와로 서로 사맛디 아니할쎄   \n한자와 서로 통하지 아니하여서    ', '틀렸습니다'))

    return lst
