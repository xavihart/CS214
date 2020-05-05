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


vector<int> SCC_set[700];   // SCC component set
vector<pair<int, int>>  Degraded_E;               // new EDGE set for graph (SCC -> vertex), vertex 1, 2, 3, ..., 666
int SCC_index[100005];


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
            //cout << t << " ";
            DFS_STACK.pop();
            visited[t] = 0;   // out ot stack

            SCC_set[num_of_scc].push_back(t);
            SCC_index[t] = num_of_scc;

        }while(t != s);
 
    }

    return;
}






void create_new_edge_set(){
    bool visited[700];
    bool connected[700][700] = {0};
    pair<int, int> new_edge;
    for(int i = 0;i < 100000;++i){
        int SCC_number = SCC_index[i];
        //cout << SCC_number << endl;
        for(int j  = heads[i]; j >= 0; j = edge_list[j].next){
           int SCC_number_2 = SCC_index[edge_list[j].v];
           if (SCC_number == SCC_number_2)
               continue;
            else{
                if(connected[SCC_number][SCC_number_2]){
                    continue;
                }else{
                    new_edge = make_pair(SCC_number, SCC_number_2);
                    Degraded_E.push_back(new_edge);
                    connected[SCC_number][SCC_number_2] = 1;
                }
            }
        }
    }
   
   ofstream f_out;
   f_out.open("Degraded_graph.out");
   for(int i = 0;i < Degraded_E.size();++i){
       f_out << Degraded_E[i].first << "," << Degraded_E[i].second << "\n";
   }
   f_out.close();

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

// check SCC_set
   int sum = 0;
   for(int i = 1; i <= rt;++i){
       sum += SCC_set[i].size();
   }

   cout << "check size: " << sum << endl;

   create_new_edge_set();

   cout << "new set created! --- edge numbers: " << Degraded_E.size() << endl;

    return rt;
}

//Please do NOT modify anything in main(). Thanks!
int main()
{
    int m,n;
    vector<pair<int,int>> edge;
    ifstream fin;
    ofstream fout;
    fin.open("SCC.in");
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
