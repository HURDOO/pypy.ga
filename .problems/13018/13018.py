# n 입력
n = int(input())
i = 2

while n > 1:

    # n을 i로 나눌 수 있다면 (즉, i가 n의 인수라면)
    if n % i == 0:
        print(i)  # i 출력

        # i가 더 이상 n의 인수가 아닐 때까지 나누기
        while n % i == 0:
            n = n // i

    # 위에서 이미 n에 i가 없다는 것이 확실해졌기 때문에, 소수인지는 따로 판별하지 않아도 됩니다.
    # 예를 들어, i=4라고 해도 이미 i=2일때 n에서 2가 모두 나뉘어졌기 때문에 나눌수가 없죠.
    # 그렇기 때문에 그냥 1만 더해줘도 됩니다.
    i = i+1

"""
// 아래는 C언어 정답 코드입니다.

#include <stdio.h>

int main()
{
    int n;
    scanf("%d", &n);
    
    int i=2;
    while (n>1) {
        if (n%i == 0) {
            printf("%d\n", i);
            
            while (n%i == 0) {
                n /= i;
            }
        }
        i += 1;
    }
    
    return 0;
}
"""
