# 자연수 n 입력
n = int(input())

# 총 n개의 줄에 걸쳐 출력
for i in range(n):

    # 합을 저장하는 sum 변수
    sum = 0

    # 1부터 i까지 모두 더하기.
    # 컴퓨터는 0부터 센다는 것을 항상 잊지 말아요!!
    for j in range(i+1):
        # sum에는 계속
        sum = sum + j + 1
