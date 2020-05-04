#include<iostream>
#include<cstdio>
#include<cstring>
#include<queue>
#include <fstream>
using namespace std;
#define maxn 500010

struct Node{
	int ne;
	int to;
	int w;  
	int co;
}e[maxn];


int head[maxn],cnt;
bool vis[maxn];
int n,m,s,t,x,y,z,f;
int dis[maxn],pre[maxn],last[maxn],flow[maxn];
int maxflow,mincost;


queue<int>q;

void add(int u,int v,int capacity,int cost)
{
	e[cnt].to = v;
	e[cnt].ne = head[u];
	e[cnt].w = capacity;
	e[cnt].co = cost;
	head[u] = cnt ++;
}


bool spfa(int s,int t)
{
	memset(dis,0x7f,sizeof(dis));
	memset(flow,0x7f,sizeof(flow));
	memset(vis,0,sizeof(vis));
	q.push(s);
	vis[s] = 1;
	dis[s] = 0;
	pre[t] = -1;
	while(!q.empty())
	{
		int now = q.front();
		q.pop();
		vis[now] = 0;
		for(int i=head[now];i > 0;i=e[i].ne)
		{
			int k =e[i].to; 
			if(e[i].w != 0 && dis[k] > dis[now]+e[i].co)
			{
				dis[k] = dis[now] + e[i].co; // 更新一下最小花费
				pre[k] = now; // 记录前驱
				last[k] = i; //与 k 相连的前一条边
				flow[k] = min(flow[now],e[i].w);
				if(!vis[k])
				{
					vis[k] = 1;
					q.push(k);
				}
			}
		}
	}
	return pre[t] != -1;// 判断能否达到汇点
}
void MCMF()
{
	while(spfa(s,t))
	{
		int now = t;
		maxflow += flow[t];
		mincost += flow[t]*dis[t];
		while(now!=s)
		{
			e[last[now]].w -= flow[t];
			e[last[now]^1].w += flow[t];
			now = pre[now];
		}
	}
}
int main()
{
	memset(head,-1,sizeof(head));
	cnt = 0;
    ifstream fin;
    ofstream fout;
    fin.open("MCMF.in");
	fin >> n >> m >> s >> t;
	for(int i=1;i<=m;i++)
	{   
		fin >> x >> y >> z >> f;
		add(x,y,z,f);
		add(y,x,0,-f);
	}
    cout << m <<" "<< n << endl;
    fin.close();
    fout.open("MCMF.out");
	MCMF();
    cout << "done\n";
	fout << maxflow << " "<< mincost << "\n";
    fout.close();
    system("pause");
	return 0;
}
