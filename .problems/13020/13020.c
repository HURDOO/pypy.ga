// 이 문제는 별도의 해설이 제공되지 않습니다. C언어 정답 코드만 제공되며, 관련 알고리즘은 '그래프' 및 '플로이드-와샬'입니다.

// 아래는 C언어 정답 코드입니다. by 박도현
#include <stdio.h>

int main() {
    int N, M, K, a, b, tmp, sum, max, max_num;
    bool arr[101][101]={0};
    int dist[101][101], m[101][101]={0};
    scanf("%d %d %d", &N, &M, &K);
    for (int i=1;i<=N;i++) {
        for (int j=1;j<=N;j++) {
            dist[i][j]=100000000;
            if (i==j) dist[i][j]=0;
        }
    }
    for (int i=0;i<K;i++) {
        scanf("%d %d", &a, &b);
        dist[a][b]=1;
        dist[b][a]=1;
    }



    for (int k=1;k<=N;k++) {
        for (int j=1;j<=N;j++) {
             for (int i=1;i<=N;i++) {
                tmp=dist[i][k]+dist[k][j];
                if (dist[i][j]>tmp) {
                    dist[i][j]=tmp;
                    dist[j][i]=tmp;
                }
            }
        }
    }

    for (int i=1;i<=N;i++) {
        for (int j=1;j<=N;j++) {
            if (M-dist[i][j]>0)
                m[i][j]=M-dist[i][j];
        }
    }

    max=0;
    for (int i=1;i<=N;i++) {
        sum=0;
        for (int j=1;j<=N;j++) {
            sum+=m[i][j];
        }
        if (max<sum) {
            max=sum;
            max_num=i;
        }
    }
    printf("%d\n%d", max_num, max);
    return 0;
}