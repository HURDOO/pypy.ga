"""
    조건이 충족되지 않았을 때, else를 이용해서 특정 코드를 실행할 수 있습니다.
"""

# 변경할 비밀번호를 입력받기
password_change = input()

# 비밀번호 확인 입력받기
password_check = input()

if password_change == password_check:
    print("비밀번호가 변경되었습니다")
else:
    print("비밀번호를 다시 확인해주세요")
