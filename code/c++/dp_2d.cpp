#include <iostream>
#include <fstream>
#include <chrono>
#include <math.h>
using namespace std;
using namespace chrono;
string* result[2];
string query[9];
string database[100];
string** read_data() {

    string filePath1 = "C:\\Users\\23769\\CLionProjects\\homework_suanfa\\MSA_database.txt";
    string filePath2 = "C:\\Users\\23769\\CLionProjects\\homework_suanfa\\MSA_query.txt";
    ifstream file1;
    ifstream file2;
    file1.open(filePath1, ios::in);
    file2.open(filePath2, ios::in);
    if (!file1.is_open() ||!file2.is_open()){
        cout<<"打不开文件";
        return 0;
    }
    string strLine;
    int i = 0;
    while (getline(file1, strLine)) {
        //cout << strLine<<endl;
        database[i++] = strLine;
    }
    file1.close();
    i = 0;
    while (getline(file2, strLine)) {
        //cout<< strLine<<endl;
        query[i++] = strLine;
    }
    file2.close();

    result[0]=query;
    result[1]=database;

}

void score_matrix_2d(int **dp,string s1,string s2){
    int n = s1.size(), m = s2.size();//n行m列
    //cout << n << m;

    for (int i = 0; i <= m; i++) {
        dp[0][i] = 2 * i;
    }
    for (int i = 0; i <= n; i++) {
        dp[i][0] = 2 * i;
    }
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i - 1] == s2[j - 1])
                dp[i][j] = min(min(dp[i - 1][j - 1], dp[i - 1][j] + 2), dp[i][j - 1] + 2);
            else
                dp[i][j] = min(min(dp[i - 1][j - 1] + 3, dp[i - 1][j] + 2), dp[i][j - 1] + 2);
        }
    }
    //return dp[n*m];
//    cout << n << m;
//    cout << "min=" << dp[n][m] << endl;
}

int score_matrix(string s1,string s2){
    int n = s1.size(), m = s2.size();//n行m列
    int dp[n + 1][m + 1];
    //cout << n << m;

    for (int i = 0; i <= m; i++) {
        dp[0][i] = 2 * i;
    }
    for (int i = 0; i <= n; i++) {
        dp[i][0] = 2 * i;
    }
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i - 1] == s2[j - 1])
                dp[i][j] = min(min(dp[i - 1][j - 1], dp[i - 1][j] + 2), dp[i][j - 1] + 2);
            else
                dp[i][j] = min(min(dp[i - 1][j - 1] + 3, dp[i - 1][j] + 2), dp[i][j - 1] + 2);
        }
    }
    return dp[n][m];
//    cout << n << m;
//    cout << "min=" << dp[n][m] << endl;
}

int   ** initialize_2d(int side,int height) {

    int **array;
    int i, j;
    array = new int *[side];//申请side个面
    for (i = 0; i < side; i++)   //对每个面申请height行
    {
        array[i] = new int[height];
        //array[i]={0};
    }
    return array;

}

int main() {
    read_data();
//    for (int i = 0; i <= 9; i++) {
//        cout << result[0][i] << endl;
//    }

//    string s1="IPJTUMAOULBGAIJHUGBSOWBWLKKBGKPGTGWCIOBGXAJLGTWCBTGLWTKKKYGWPOJL";
//    string s2="KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX";
    string s1 = "FWKPHPJTJJPJAPPJJHKJPKPJJPPJAPPJJJPKJJKKJJPPAJJHPJJPPAJJPPOJKPJJJ";
    string s2 = "IPUTAMPOJOPOMLXHOOOMUQBOTIKOHVWJJKSHPWZXUSVPPQSPBUPPKAKWSOGPSJLWWZJUJPPOZJTOGUTPKJPGJ";
    std::chrono::steady_clock::time_point  t1 = std::chrono::steady_clock::now();
    for (int i=1;i<=5;i++){
        int best_score;
        int index_data=0;
        for (int j=0;j<=99;j++){
            if (j==0)
                best_score=score_matrix(query[i],database[j]);
            else {
                if (best_score>score_matrix(query[i],database[j])){
                    best_score=score_matrix(query[i],database[j]);
                    index_data=j;
                }
            }
        }
        cout<<"序列"<<query[i]<<"最匹配的序列为："<<database[index_data]<<'  '<<"cost为："<<best_score<<endl;
    }
    std::chrono::steady_clock::time_point  t2 = std::chrono::steady_clock::now();
    auto time_span = std::chrono::duration_cast<microseconds>(t2 - t1);

    std::cout << "It took me " << time_span.count()/pow(10,6) << " seconds.";
    std::cout << std::endl;
//    int n = s1.size(), m = s2.size();//n行m列
//    int **dp= initialize_2d(n+1,m+1);
//    //int dp[n + 1][m + 1];
//    score_matrix_2d(dp,s1,s2);
//    cout<<dp[n][m]<<endl;

    return 0;
}
