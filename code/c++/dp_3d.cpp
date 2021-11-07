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
int theta_3d(char a, char b,char c) {
    if (a == '-' &&b == '-'&& c == '-' ){
        cout<<"出错";
        return -1;
    }

    else if (a == '-' &&b == '-' || a == '-' && c == '-' || c == '-'&& b == '-')
        return 4;

    else if (a == '-')
    {

        if (b == c)
            return 4;
        else
            return 7;
    }

    else if (b == '-')
    {

        if (a == c)
        return 4;
        else
        return 7;
    }

    else if (c == '-')
    {

        if (a == b)
        return 4;
        else
        return 7;
    }

    else if (a == b && a == c) {
        return 0;
    }

    else if (a != b && a != c && b != c)
        return 9;

    else
    return 6;
}
void test(int* dp,int row ,int col){
    for (int i=1;i<row*col;i++){
        if(i%col==0&&i<=col)cout<<i<<endl;
        if (dp[i]==0){
//cout<<i<<"出错"<< endl;
return;
}
    }
}
int   *** initialize_3d(int side,int height,int width) {

    int ***array;

    int i, j;

    array = new int **[side];//申请side个面
    for (i = 0; i < side; i++)   //对每个面申请height行
    {
        array[i] = new int *[height];

        for (j = 0; j < height; j++)   //对每行申请width列
            array[i][j] = new int[width];
        //array[i][j]={0};
    }
    return array;

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
int score_matrix_3d(string s1,string s2, string s3){
    int n = s1.size(), m = s2.size(),z=s3.size();//n行m列
//    cout<<'n'<<n<<'m'<<m<<'z'<<z<<endl;
//    int dp[n + 1][m + 1][z+1];
//    initialize((int*)dp,(n+1)*(m + 1)*(z+1));
////    if ( NULL == dp )cout<<"dp出错";
////    cout<<"1到这没问题";
//    int dp12[n + 1][m + 1];
//    initialize((int*)dp12,(n+1)*(m + 1));
////    if ( NULL == dp12 )cout<<"dp12出错";
////    cout<<"2到这没问题";
//    int dp13[n + 1][z+1];
//    initialize((int*)dp13,(n+1)*(z+1));
////    if ( NULL == dp13 )cout<<"dp13出错";
//    int dp23[m + 1][z + 1];
//    initialize((int*)dp23,(m + 1)*(z+1));
//    if ( NULL == dp23 )cout<<"dp23出错";
    //cout << n << m;
//    cout<<"3到这没问题";

    int ***dp=initialize_3d(n+1,m+1,z+1);
    int **dp12= initialize_2d(n+1,m+1);
    int **dp13= initialize_2d(n+1,z+1);
    int **dp23=initialize_2d(m+1,z+1);
    score_matrix_2d(dp12,s1,s2);
    //cout<<"4到这没问题";
    score_matrix_2d(dp13,s1,s3);
    // cout<<"5到这没问题";
    score_matrix_2d(dp23,s2,s3);
    // cout<<"6到这没问题";
    //cout<<"中间"<<dp12[1][1]<<endl;
//    test((int*)dp12,(n+1),(m+1));
//    test((int*)dp13,(n+1),(z+1));
//    test((int*)dp23,(m+1),(z+1));
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= m; j++) {
            for (int k = 0; k <= z; k++) {
                if (i == 0) {
                    dp[i][j][k] = dp23[j][k] + 2 * (j + k);
                    continue;
                }
                if (j == 0) {
                    dp[i][j][k] = dp13[i][k] + 2 * (i + k);
                    continue;
                }
                if (k == 0) {
                    dp[i][j][k] = dp12[i][j] + 2 * (i + j);
                    continue;
                }
                int d1, d2, d3, d4, d5, d6, d7;
                d1 = dp[i][j][k - 1] + theta_3d('-', '-', s3[k-1]);
                d2 = dp[i - 1][j][k - 1] + theta_3d('-', s1[i-1], s3[k-1]);
                d3 = dp[i - 1][j][k] + theta_3d('-', '-', s1[i-1]);
                d4 = dp[i - 1][j - 1][k] + theta_3d('-', s1[i-1], s2[j-1]);
                d5 = dp[i][j - 1][k] + theta_3d('-', '-', s2[j-1]);
                d6 = dp[i][j - 1][k - 1] + theta_3d('-', s2[j-1], s3[k-1]);
                d7 = dp[i - 1][j - 1][k - 1] + theta_3d(s1[i-1], s2[j-1], s3[k-1]);
                dp[i][j][k] = min(min(min(min(min(min(d5, d6), d7), d4), d3), d2), d1);
                //cout<<"i"<<i<<"j"<<j<<"k"<<k<<"cost"<<dp[i][j][k]<<endl;


//    cout << n << m;
//    cout << "min=" << dp[n][m] << endl;
            }
        }
    }
    return dp[n][m][z];
}
int main() {
    read_data();
//    for (int i = 0; i <= 9; i++) {
//        cout << result[0][i] << endl;
//    }

    //string s1="IPJTUMAOULBGAIJHUGBSOWBWLKKBGKPGTGWCIOBGXAJLGTWCBTGLWTKKKYGWPOJL";
 //string s2="KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX";

//    string s1 = "FWKPHPJTJJPJAPPJJHKJPKPJJPPJAPPJJJPKJJKKJJPPAJJHPJJPPAJJPPOJKPJJJ";
//    string s2 = "IPUTAMPOJOPOMLXHOOOMUQBOTIKOHVWJJKSHPWZXUSVPPQSPBUPPKAKWSOGPSJLWWZJUJPPOZJTOGUT";
//    string s3 = "JJXPSPJAHATJAJXHAAJXJXOOGPPPAPHJJHAHJJAKXRJJAPAPAJJPPAPJOPPAJJS";
    //string s3 ="VXTLKZOKMOKAPHXHMLOWZHTPPHKPKIAXPOXKSKSWJSTSGNSHIOTTLPLLMZKUJHXTPWOWHZGAHLWKKPKMPXOTMZJUOPJ";
    std::chrono::steady_clock::time_point  t1 = std::chrono::steady_clock::now();
//    int cost=score_matrix_3d(s1,s2,s3);
//    cout<<cost;



    for (int i=7;i<=8;i++){
        int best_score;
        int indexj_data=0;
        int indexk_data=0;
        int score;

        for (int j=0;j<=98;j++){
            for (int k=j+1;k<=99;k++){
            if (j==0 &&k==1) {
                //cout<<database[k]<<endl;
                best_score = score_matrix_3d(query[i], database[j], database[k]);
                //cout<<"best_score"<< best_score<<endl;
            }
            else {
                //cout<<database[k]<<endl;
                //cout<<query[i]<<endl<<database[j]<<endl<<database[k]<<endl;
                score=score_matrix_3d(query[i],database[j],database[k]);
                //cout<<"score"<< score<<endl;
                if (best_score > score) {
                    //cout<< "替换了"<<endl;
                    best_score = score;
                    indexj_data = j;
                    indexk_data = k;
                 }
                }
            }
        }
        cout<<"序列"<<query[i]<<"最匹配的两个序列为："<<endl<<database[indexj_data]<<"和"<<endl<<database[indexk_data]<<endl<<"cost为："<<best_score<<endl;
    }




    std::chrono::steady_clock::time_point  t2 = std::chrono::steady_clock::now();
    auto time_span = std::chrono::duration_cast<microseconds>(t2 - t1);

    std::cout << "It took me " << time_span.count()/pow(10,6) << " seconds.";
    std::cout << std::endl;
    return 0;
}
