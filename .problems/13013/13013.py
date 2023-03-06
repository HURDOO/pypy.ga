# 첫번째 숫자 입력
a = int(input())

# 기호 입력
sign = input()

# 두번째 숫자 입력
b = int(input())

if sign == '+':
    print(a+b)
elif sign == '-':
    print(a-b)
elif sign == '*':
    print(a*b)
else:
    print(a/b)

# 참고: elif는 else if의 줄임말이에요. 위의 조건이 충족되지 않을 때, 다른 조건을 다시 걸어주는 명령어랍니다.
# 물론 elif랑 else 안 쓰고, 아래처럼 써도 동일하게 작동해요.
"""
if sign == '+':
    print(a+b)
if sign == '-':
    print(a-b)
if sign == '*':
    print(a*b)
if sign == '/':
    print(a/b)
"""
