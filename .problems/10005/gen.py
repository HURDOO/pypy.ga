import os
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = []
    for s in '우영우, 동그라미, 사공용욱, 남석희, 송선호, 황종철, 정우정, 예우철, 김정우, 홍경철' \
             ', 배창민, 양희선, 윤재혁, 최준기, 사공희용, 조광민, 정정환, 유소민, 제갈은재, 예범수' \
             ', 안동훈, 고준민, 양원숙, 오병호, 윤정원, 하지원, 사공원주, 한시은, 설소희, 표혜은' \
             ', 복은기, 고승태, 정남희, 서인철, 정영태, 남성현, 송정환, 류준호, 권준식, 송서연' \
             ', 사공나길, 조샘, 안한길, 안달, 성으뜸, 황으뜸, 백나라우람, 강나라우람, 박나길, 복믿음' \
             ', 황한결, 전우람, 윤버들, 손미르, 김미르, 서나길, 예우람, 권버들, 표나라우람, 탁버들' \
             ', 문새롬, 서초롱, 전겨울, 강다솜, 전새롬, 박겨울, 노슬기, 제갈달래, 황아리, 이단비' \
             ', 남궁구슬, 강민들레, 한아라, 황보그루, 조나비, 복라온, 봉나빛, 추바다, 표한별, 손가람' \
             ', 홍성한, 한재범, 추경택, 예강민, 황철순, 송이수, 박성한, 백철순, 문요한, 류강민' \
             ', 오자경, 유이경, 조애정, 류경님, 하은채, 서지해, 황혜린, 남궁자경, 최영애, 복영신'\
            .split(', '):
        lst.append((s, s[0] + ' to the ' + s[1] + ' to the ' + s[2:]))
    return lst


PROBLEM_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROBLEM_DIR / 'in'
OUTPUT_DIR = PROBLEM_DIR / 'out'
INPUT_FILENAME = '{}.in'
OUTPUT_FILENAME = '{}.out'

if not os.path.exists(INPUT_DIR):
    os.mkdir(INPUT_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

case_list = get_input_output()

for idx in range(len(case_list)):
    stdin, stdout = case_list[idx]
    with open(INPUT_DIR / INPUT_FILENAME.format(idx + 1), 'w', encoding='UTF-8') as input_file:
        input_file.write(stdin + '\n')
    with open(OUTPUT_DIR / OUTPUT_FILENAME.format(idx + 1), 'w', encoding='UTF-8') as output_file:
        output_file.write(stdout + '\n')
