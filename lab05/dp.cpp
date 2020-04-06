#include<iostream>
#include<cstring>
using namespace std;
int dp[2005][4005];
int min_(int a, int b){return a > b ? b : a;}
int main(){
    int n;
    int w[2005];
    int t[2005];
    cin >> n;
    for(int i = 1;i <= n;++i){
        cin >> t[i] >> w[i];
    }

    for(int i = 0;i < 2005;++i)
       for(int j = 0;j < 4005;++j)
           dp[i][j] = 3 * n;

    dp[0][0] = 0;

    
    cout << dp[0][1] << endl;
    int tmp = 0;
    for(int i = 1; i <= n;++i){
        tmp += t[i];
        for(int j = 1;j <= tmp;++j){
           dp[i][j] = dp[i - 1][j] + w[i];

           if(j - t[i] >= 0){
               dp[i][j] = min_(dp[i][j], dp[i - 1][j - t[i]]);
           }
        }
    }


    for(int i = 1;i <= n * 2;++i){
        if(dp[n][i] <= i){
            cout << i << endl;
            break;
        }
    }
   
          
        system("pause");
        return 0;
        
}