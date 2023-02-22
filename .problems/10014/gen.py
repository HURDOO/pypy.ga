import random
import string


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    random.seed(10014)

    for _ in range(60):
        num = random.randint(0, 101)
        s1 = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ')
                     for _ in range(random.randint(0, num*2)))
        s2 = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ')
                     for _ in range(random.randint(0, num)))
        lst.append((f'{s1}\n{s2}', (lambda: '출력 초과' if len(s1) > 2*len(s2) else '채점 중')()))

        if len(s1) > 2*len(s2):
            print('casd')

    random.shuffle(lst)

    lst.insert(0, ('abcd\nabcd', '채점 중'))
    lst.insert(1, ('1234567890\n1234', '출력 초과'))

    return lst
