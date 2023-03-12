# 자연수 n 입력
n = int(input())

# i는 0부터 8까지 반복
for i in range(9):
    # n은 입력받은 수, i+1은 1부터 9까지 반복
    # 문자와 숫자는 더할 수 없으므로, 숫자를 문자로 바꿔서 더하기
    print(str(n) + "x" + str(i+1) + " = " + str(n*(i+1)))

    # 면접에서는 그냥 아래 코드로 숫자만 출력해도 무방했습니다.
    # print(n*(i+1))


"""
// 아래는 C언어 정답 코드입니다.
    
#include <stdio.h>

int main()
{
    int n;
    scanf("%d", &n);
    
    for (int i=1;i<10;i++) {
        printf("%d*%d = %d\n", n, i, n*i);
    }
    
    return 0;
}
"""