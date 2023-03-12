"""
    이 문제에는 3가지 풀이 방법이 존재합니다.
    1. 진법을 이용한 풀이  (모범 답안)
    2. 리스트를 이용한 풀이
    3. 재귀함수를 이용한 풀이
"""

"""
    1. 진법을 이용한 풀이
    - 시간복잡도: O(log4(n))
"""
# n 입력
n = int(input())

# 최종 출력값을 나타내는 변수
answer = True

# n이 0이 될 때까지 계속 나눠봅니다.
while n > 1:
    # 1, 4, 16, 64, 256, 1024는 모두 4의 배수입니다.
    # 따라서 입력받은 무게를 4진법으로 나타내었을 때, 3이 하나라도 있다면, 추가 2개밖에 없으므로, 그 무게는 추로 표현이 불가능합니다.
    # 예를 들어, 43을 4진법으로 나타내면 '223' (=16*2 + 4*2 + 1*3) 이므로, 마지막 자리에 3이 있어 표현이 불가능합니다.
    # i진법의 마지막 자리 수는 i로 나눈 나머지로 알 수 있습니다.
    if n % 4 == 3:
        answer = False

    # 다음 자리도 알아보기 위해 i로 나눈 몫을 다시 구해줍니다. 이러면 마지막 자리가 떨어져나갑니다.
    n = n // 4

# 정답을 출력합니다
print(answer)

"""
// 아래는 C언어 정답 코드입니다.

#include <stdio.h>

int main()
{
    int n;
    scanf("%d", &n);
    
    bool answer = false;
    while (n > 1)
    {
        if (n%4 == 3)
        {
            answer = false;
            break; // 이건 선택사항
        }
        n /= 4;
    }
    
    if (answer) printf("True");
    else printf("False");
    
    return 0;
}
"""

"""
    2. 리스트를 이용한 풀이
    - 시간복잡도: O((2^6)^2)
"""

# n 입력
n = int(input())

# 잴 수 있는 모든 무게를 담을 리스트 생성
arr = [0]

# 모든 추에 대해 경우의 수 구하기
for i in [1, 4, 16, 64, 256, 1024]:

    # 추는 2개씩
    for j in range(2):

        # 지금까지 가능했던 모든 경우에 대해, 지금 이 추(i)를 사용했을 때 가능한 경우도 추가
        arr_length = len(arr)
        for k in range(arr_length):
            arr.append(arr[k] + i)

print(n in arr)

"""
// 아래는 C언어 정답 코드입니다.

#include <stdio.h>

int main()
{
    int n;
    scanf("%d", &n);
    
    int arr[4096] = {0};  // 2^12
    int arr_length = 1;
    
    for (int i=1;i<=1024;i*=4) {
        for (int j=0;j<2;j++) {
            for (int k=0;k<arr_length;k++) {
                arr[arr_length+k] = i;
            }
            arr_length *= 2;
        }
    }
    
    for (int i=0;i<4096;i++) {
        if (arr[i] == n) {
            printf("True");
            return 0;
        }
    }
    
    printf("False");
    return 0;
}
"""

"""
    3. 재귀함수를 이용한 풀이
    - 시간복잡도: O(3^log4(n))
"""

# 모든 추
arr = [1, 4, 16, 64, 256, 1024]

# n 입력
n = input()

# 정답변수 answer
answer = False


# 모든 경우의 수를 넣어보는 함수
def func(val, cnt):
    # 현재 값이 n이면 무게를 재는 것이 가능
    if val == n:
        answer = True

    # 모든 추를 다 쓰면 끝.
    if cnt > len(arr):
        return

    # 지금 이 추를 사용하지 않았을 때
    func(val, cnt + 1)

    # 지금 이 추를 1개 사용했을 때
    val += arr[cnt]
    func(val, cnt + 1)

    # 지금 이 추를 2개 사용했을 때
    val += arr[cnt]
    func(val, cnt + 1)


# 아무 추도 사용하지 않는 경우의 수부터, 모든 추를 사용하는 모든 경우의 수를 돌려봄
func(0, 0)

# 정답 출력
print(answer)

"""
// 아래는 C언어 정답 코드입니다.

#include <stdio.h>

int n, arr[6] = {1, 4, 16, 64, 256, 1024};
bool answer = false;
void func(int val, int cnt)
{
    if (val == n) answer = true;
    if (cnt == 6) return;
    
    func(val, cnt+1)
    val += arr[cnt];
    func(val, cnt+1)
    val += arr[cnt];
    func(val, cnt+1)
}

int main()
{
    int n;
    scanf("%d", &n);
    func(0, 0);
    if (answer) printf("True");
    else printf("False");
}
"""
