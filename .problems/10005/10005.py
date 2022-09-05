"""
    문자열을 다루는 문제입니다.
"""

s = input()

s = s[0] + ' to the ' + s[1:]  # 우 to the 영우
s = s[:10] + ' to the ' + s[10:]  # 우 to the 영 to the 우
print(s)
