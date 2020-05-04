#include <vector>
#include <iostream>
#include <fstream>
#include <stack>
#include<cstring>
using namespace std;
//Please put this source code in the same directory with SCC.in
//And do NOT change the file name.
/*
This function computes the number of Strongly Connected Components in a graph
Args:
    n: The number of nodes in the graph. The nodes are indexed as 0~n-1
    edge: The edges in the graph. For each element (a,b) in edge, it means
          there is a directed edge from a to b
          Notice that there may exists multiple edge and self-loop
Return:
    The number of strongly connected components in the graph.
*/

struct node {
     int v,next;
 }edge_list[500001];


int DFN[100005]={0},LOW[100005];
int heads[100005];
int visited[100005];
int count=0,total_number=0,num_of_scc=0;
stack<int> DFS_STACK;
bool init = 0;


void add(int x,int y)
{
     edge_list[++count].next=heads[x];
     edge_list[count].v = y;
     heads[x]=count;
     //cout << count << endl;
     return;
 }


void tarjan(int s){
    //cout << s << endl;
    total_number += 1;
    DFN[s] = total_number;
    LOW[s] = total_number;
    DFS_STACK.push(s);
    visited[s] = 1;
   // cout << s << endl;
    for(int i  = heads[s]; i >= 0; i = edge_list[i].next){


        if(DFN[edge_list[i].v] == 0){   // has not been visited
            tarjan(edge_list[i].v);
            if(LOW[s] > LOW[edge_list[i].v]){
                LOW[s] = LOW[edge_list[i].v];
            }
        }else if(visited[edge_list[i].v] == 1){    // still in the dfs stack
             if(LOW[s] > LOW[edge_list[i].v]){
                LOW[s] = LOW[edge_list[i].v];
            }           
        }

    }
    
    

    if(DFN[s] == LOW[s]){
        num_of_scc ++;
        int t;
        do{
            
            t = DFS_STACK.top();
            cout << t << " ";
            DFS_STACK.pop();
            visited[t] = 0;   // out ot stack
        }while(t != s);
    cout << endl;
    }

    return;
}





int SCC(int n, vector<pair<int,int>>& edge) {
    if (!init){
        memset(heads,-1,sizeof(heads));
        for(int i = 0;i < edge.size();++i){
            int s, e;
            s = edge[i].first;
            e = edge[i].second;
            add(s, e);
           // if(heads[s] == 0)
             //  cout << s;
        }
        init = !init;
    }
    cout << "init edge list done ...\n";
    //cout << edge_list[0].next << "!";
    for(int i = 0;i < n;++i){
        if(DFN[i] == 0){
            tarjan(i);
        }
    }
    int rt = num_of_scc;
    cout << "number of scc:" << rt <<endl;
   // for(int i = 0;i < n;++i){
     //   cout << DFN[i] << "  " << LOW[i] << endl;
   // }
    return rt;
}

//Please do NOT modify anything in main(). Thanks!
int main()
{
    int m,n;
    vector<pair<int,int>> edge;
    ifstream fin;
    ofstream fout;
    fin.open("myscc.in");
    fin>>n>>m;
    int tmp1,tmp2;
    for(int i=0;i<m;i++)
    {
        fin>>tmp1>>tmp2;
        edge.push_back(pair<int,int>(tmp1,tmp2));
    }
    fin.close();
    int ans=SCC(n,edge);
    fout.open("SCC.out");
    fout<<ans<<'\n';
    fout.close();
    system("pause");
    return 0;
}
