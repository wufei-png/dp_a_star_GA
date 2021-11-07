//
// Created by 23769 on 2021/10/31.
//

#include <iostream>
#include <fstream>
#include <chrono>
#include <math.h>
#include <queue>
#include <vector>
#include <functional>
#include <map>
using std::map;
using namespace std;
using namespace chrono;
string* result[2];
string query[9];
string database[100];

class Node
{
public:
    int x, y,z,cost;
    Node(){}
    Node(int x, int y,int z,int cost) : x(x), y(y),z(z),cost(cost) {}

    bool operator<(const Node &a) const		//方法1：重载运算符
    {
        return cost < (a.cost);
    }

    bool operator>(const Node &a) const
    {
        return cost > (a.cost);
    }
};

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




string combin(int i,int j,int k){

    string a=to_string(i);
    string b=to_string(j);
    string c=to_string(k);
    string d=a+ '+' + b + '+' + c;

    return d;


}

void store(map<string, int>& map1,Node node,int value){
    string c= combin(node.x,node.y,node.z);
    map1[c]=value;
    //cout<<map1[c];
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

int cost_point_to_point(Node node1,int direction,string seq1,string seq2,string seq3){

    if (direction==1||direction==3 || direction==5)
        return 4;

    if (direction==2) {
        if (seq1[node1.x] == seq3[node1.z])
            return 4;
        else
            return 7;
    }
    if (direction==4){
        if (seq1[node1.x]==seq2[node1.y])
            return 4;
        else
            return 7;
    }
    if (direction==6) {
        if (seq2[node1.y] == seq3[node1.z])
            return 4;
        else
            return 7;
    }
    if (direction==7)
        return theta_3d(seq1[node1.x],seq2[node1.y], seq3[node1.z]);
}
int fromwhere(Node node1,Node node2){

    int i1=node1.x;
    int j1=node1.y;
    int k1=node1.z;
    int i=node2.x;
    int j=node2.y;
    int k=node2.z;
    if (i1==i &&j1==j &&k1+1==k)
        return 1;
    if (i1+1==i && j1==j &&k1+1==k)
        return 2;
    if (i1+1==i && j1==j && k1==k)
        return 3;
    if (i1+1==i && j1+1==j && k1==k)
        return 4;
    if (i1==i && j1+1==j &&k1==k)
        return 5;
    if (i1==i && j1+1==j && k1+1==k)
        return 6;
    if (i1+1==i && j1+1==j && k1+1==k)
        return 7;

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

int H_cost(Node next,int* size,int **dp12,int **dp13,int **dp23) {
//    if (direction == 1) {
//
//        seq3.erase(0, 1);
//
//    }
//
//    if (direction == 2) {
//        seq1.erase(0, 1);
//
//        seq3.erase(0, 1);
//
//    }
//    if (direction == 3) {
//        seq1.erase(0, 1);
//
//
//    }
//    if (direction == 4) {
//        seq1.erase(0, 1);
//        seq2.erase(0, 1);
//
//
//    }
//    if (direction == 5) {
//
//        seq2.erase(0, 1);
//
//
//    }
//    if (direction == 6) {
//
//        seq2.erase(0, 1);
//        seq3.erase(0, 1);
//
//    }
//    if (direction == 7) {
//        seq1.erase(0, 1);
//        seq2.erase(0, 1);
//        seq3.erase(0, 1);
//
//    }
    int i=next.x;
    int j=next.y;
    int k=next.z;
    //cout<<size[0]<<size[1]<<size[2];
    //cout<<dp12[size[0]][size[1]];
    int score12=dp12[size[0]][size[1]]-dp12[i][j];
    int score13=dp13[size[0]][size[2]]-dp13[i][k];
    int score23=dp23[size[1]][size[2]]-dp23[j][k];
    return score12+score13+score23;
//    return dp[size[0]][size[1]][size[2]]-dp[i][j][k];
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

int score_matrix_3d(int ***dp,string s1,string s2, string s3){
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

}

int astar(string seq1,string seq2,string seq3){


    int n=seq1.size();
    int m=seq2.size();
    int z=seq3.size();
//    int ***dp=initialize_3d(n+1,m+1,z+1);
//    score_matrix_3d(dp,seq1,seq2,seq3);
    int **dp12= initialize_2d(n+1,m+1);
    int **dp13= initialize_2d(n+1,z+1);
    int **dp23=initialize_2d(m+1,z+1);
    score_matrix_2d(dp12,seq1,seq2);
    //cout<<"4到这没问题";
    score_matrix_2d(dp13,seq1,seq3);
    // cout<<"5到这没问题";
    score_matrix_2d(dp23,seq2,seq3);


    priority_queue<Node, vector<Node>,greater<Node> > pq;
    int size[3];
    size[0]=seq1.size();
    size[1]=seq2.size();
    size[2]=seq3.size();
    Node start(0,0,0,0);
    string goal=combin(seq1.size(),seq2.size(),seq3.size());
    pq.push(start);
    map<string, int> cost_so_far;
    store(cost_so_far,start,0);
    while(!pq.empty()){
        Node current=pq.top();
        pq.pop();
        if(current.x==seq1.size()&&current.y==seq2.size()&&current.z==seq3.size())
            break;
        int i=current.x;
        int j=current.y;
        int k=current.z;
        Node* newnodes=new Node[7];






        int count;
        Node Node1(current.x+1,current.y,current.z,0);
        Node Node2(current.x,current.y+1,current.z,0);
        Node Node3(current.x,current.y,current.z+1,0);
        Node Node4(current.x,current.y+1,current.z+1,0);
        Node Node5(current.x+1,current.y+1,current.z,0);
        Node Node6(current.x+1,current.y,current.z+1,0);
        Node Node7(current.x+1,current.y+1,current.z+1,0);
        if (i+1<=seq1.size() && j+1<=seq2.size()&& k+1<=seq3.size()) {
            count=7;
            newnodes[0] = Node1;
            newnodes[1] = Node2;
            newnodes[2] = Node3;
            newnodes[3] = Node4;
            newnodes[4] = Node5;
            newnodes[5] = Node6;
            newnodes[6] = Node7;

        }
        else if (i+1<=seq1.size() && j+1<=seq2.size()&& k+1>seq3.size()) {
            count=3;
            newnodes[0] = Node1;
            newnodes[1] = Node2;
            newnodes[2] = Node5;


        }
        else if (i+1>seq1.size() && j+1<=seq2.size()&& k+1<=seq3.size()) {
            count = 3;
            newnodes[0] = Node2;
            newnodes[1] = Node3;
            newnodes[2] = Node4;
        }
        else if (i+1<=seq1.size() && j+1>seq2.size()&& k+1<=seq3.size()) {
            count = 3;
            newnodes[0] = Node1;
            newnodes[1] = Node3;
            newnodes[2] = Node6;
        }
        else if (i+1>seq1.size() && j+1>seq2.size()&& k+1<=seq3.size()) {
            count = 1;
            newnodes[0] = Node3;
        }
        else if (i+1<=seq1.size() && j+1>seq2.size()&& k+1>seq3.size()) {
            count = 1;
            newnodes[0] = Node1;
        }
        else if (i+1>seq1.size() && j+1<=seq2.size()&& k+1>seq3.size()) {
            count = 1;
            newnodes[0] = Node2;
        }
        else
        {
            cout<<"出错";
            return -1;
        }



        for (int i=0;i<count;i++){


            int direction = fromwhere(current,newnodes[i]);
            //cout<<direction;
            int newcost=cost_so_far[combin(current.x,current.y,current.z)]+ cost_point_to_point(current,direction,seq1,seq2,seq3);

            string newnode= combin(newnodes[i].x,newnodes[i].y,newnodes[i].z);

//            std::chrono::steady_clock::time_point  t3 = std::chrono::steady_clock::now();
            //cout<<newnode<<endl;
            if (cost_so_far.find(newnode) ==cost_so_far.end()||newcost<cost_so_far[newnode])
            {//0.22

                //cout<<H_cost(seq1,seq2,seq3,direction)<<endl;
//                std::chrono::steady_clock::time_point  t4 = std::chrono::steady_clock::now();
//                auto time_span2 = std::chrono::duration_cast<microseconds>(t4 - t3);
//                time_count2+=time_span2.count();
                newnodes[i].cost=newcost+ H_cost(newnodes[i],size,dp12,dp13,dp23);
                //store(cost_so_far,newnodes[i],newcost);
                cost_so_far[newnode]=newcost;
                pq.push(newnodes[i]);

            }

        }
    }//std::cout << "It took me " << time_count1 << " seconds.";
    // std::cout << "It took me " << time_count2/pow(10,6) << " seconds.";
    return cost_so_far[goal];
}

//cout<<pq.top().x<<pq.top().y;




int main(){
    read_data();
    std::chrono::steady_clock::time_point  t1 = std::chrono::steady_clock::now();
    string s1 = "IPZJJLMLTKJULOSTKTJOGLKJOBLTXGKTPLUWWKOMOYJBGALJUKLGLOSVHWBPGWSLUKOBSOPLOOKUKSARPPJ";
    string s2 = "IPJTUMAOULBGAIJHUGBSOWBWLKKBGKPGTGWCIOBGXAJLGTWCBTGLWTKKKYGWPOJL";
    string s3 = "BNIPMBSKHSASLLXKPIPLPUVHKHCSJCYAPLUKJGSGPGSLKUBDXGOPKLTLUCWKAUSL";
//    std::chrono::steady_clock::time_point  t3 = std::chrono::steady_clock::now();

//    std::chrono::steady_clock::time_point  t4 = std::chrono::steady_clock::now();
//    auto time_span1 = std::chrono::duration_cast<seconds>(t3 - t4);
//    std::cout << "It took me " << time_span1.count() << " seconds.";
    cout<<astar(s1,s2,s3);
    std::chrono::steady_clock::time_point  t2 = std::chrono::steady_clock::now();
    auto time_span2 = std::chrono::duration_cast<seconds>(t2 - t1);

    std::cout << "It took me" << time_span2.count() << " seconds.";
    std::cout << std::endl;
//    string s1="abc";
//    string s2="ab";
////    string s1="abc";
////    string s2="bcd";
//    cout<<astar(s1,s2);
}


