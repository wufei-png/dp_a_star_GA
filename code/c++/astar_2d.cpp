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
    int x, y,cost;
    Node(){}
    Node(int x, int y,int cost) : x(x), y(y),cost(cost) {}

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

string combin(int i,int j){
    string a=to_string(i);
    string b=to_string(j);
    string c=a+'+'+b;
    return c;
}

void store(map<string, int>& map1,Node node,int value){
    string c= combin(node.x,node.y);
    map1[c]=value;
    //cout<<map1[c];
}

int cost_point_to_point(Node node1,int direction,string seq1,string seq2){

    if (direction==0){
        if (seq1[node1.x]==seq2[node1.y])
            return 0;
        else return 3;
    }
    else return 2;
}
int fromwhere(Node node1,Node node2){
    if ((node1.x==node2.x)&&(node1.y+1==node2.y))
        return 1;

    else if ((node1.x+1==node2.x)&&(node1.y+1==node2.y))
    return 0;

    else if ((node1.x+1==node2.x)&&(node1.y==node2.y))
        return 2;
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

int H_cost(Node next,int* size,int **dp) {
//    if (direction == 0) {
//        seq1.erase(0, 1);
//        seq2.erase(0, 1);
//    }
//    if (direction == 1) {
//
//        seq2.erase(0, 1);
//    }
//    if (direction == 2) {
//        seq1.erase(0, 1);
//
//    }
int i=next.x;
int j=next.y;
//cout<<dp[size[0]][size[1]];
    return dp[size[0]][size[1]]-dp[i][j];
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

int astar(string seq1,string seq2){
//    int time_count;
    int n=seq1.size();
    int m=seq2.size();
    int size[2];
    size[0]=n;
    size[1]=m;
    int **dp= initialize_2d(n+1,m+1);

    score_matrix_2d(dp,seq1,seq2);

    priority_queue<Node, vector<Node>, greater<Node> > pq;

    Node start(0,0,0);
    string goal=combin(seq1.size(),seq2.size());
    pq.push(start);
    map<string, int> cost_so_far;
    store(cost_so_far,start,0);
    while(!pq.empty()){
        Node current=pq.top();
        pq.pop();
        if(current.x==seq1.size()&&current.y==seq2.size())
            break;
        int i=current.x;
        int j=current.y;
        Node* newnodes=new Node[3];
        int count;
        Node Node1(current.x,current.y+1,0);
        Node Node2(current.x+1,current.y,0);
        Node Node0(current.x+1,current.y+1,0);
        if (i+1<=seq1.size() && j+1<=seq2.size()) {
            count=3;
            newnodes[0] = Node0;
            newnodes[1] = Node1;
            newnodes[2] = Node2;
        }
        else if (i+1<=seq1.size() && j+1>seq2.size()) {
            count = 1;
            newnodes[0] = Node2;
        }
        else if (i+1>seq1.size() && j+1<=seq2.size()) {
            count = 1;
            newnodes[0] = Node1;
        }

        for (int i=0;i<count;i++){

            int direction = fromwhere(current,newnodes[i]);
            int newcost=cost_so_far[combin(current.x,current.y)]+ cost_point_to_point(current,direction,seq1,seq2);
            string newnode= combin(newnodes[i].x,newnodes[i].y);
            if (cost_so_far.find(newnode) ==cost_so_far.end()||newcost<cost_so_far[newnode])
            {
                cost_so_far[newnode]=newcost;
//                std::chrono::steady_clock::time_point  t1 = std::chrono::steady_clock::now();
                newnodes[i].cost=newcost+ H_cost(newnodes[i],size,dp);
//                std::chrono::steady_clock::time_point  t2 = std::chrono::steady_clock::now();
//                auto time_span = std::chrono::duration_cast<seconds>(t2 - t1);
//                time_count+=time_span.count();
                pq.push(newnodes[i]);
            }
        }
        }


//    std::cout << "It took me " << time_count << " seconds.";
    return cost_so_far[goal];
    }

    //cout<<pq.top().x<<pq.top().y;




int main(){
    read_data();
        std::chrono::steady_clock::time_point  t1 = std::chrono::steady_clock::now();
    for (int i=1;i<=5;i++){
        int best_score;
        int index_data=0;
        int score;
        for (int j=0;j<=99;j++){
            if (j==0)
                best_score=astar(query[i],database[j]);
            else {
                score=astar(query[i],database[j]);
                if (best_score>score){
                    best_score=score;
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
//    string s1="IPZJJLMLTKJULOSTKTJOGLKJOBLTXGKTPLUWWKOMOYJBGALJUKLGLOSVHWBPGWSLUKOBSOPLOOKUKSARPPJ";
//    string s2="IPOKJOLKHPZUOZJOGGUSPXLOHLTUTOGKJOTOXPGGZPGPVPHOSOJMOJOSIOMGCWWOWUPPPOGULWHVLJGKPLMMMMMMMMDDDDDDDDDDDDDDDDDDDDDDDDDD";
////    string s1="abc";
////    string s2="bcd";
//    cout<<astar(s1,s2);
}


