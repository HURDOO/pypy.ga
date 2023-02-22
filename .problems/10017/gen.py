import random
import string


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    sentence = 'There is a major problem with counting from 0.'

    for word in string.ascii_letters + string.digits + string.punctuation:
        lst.append((word, str(sentence.find(word))))

    random.seed(10017)
    random.shuffle(lst)

    return lst
