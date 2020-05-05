#include<iostream>
#include<cstdio>
#include<cstring>
#include<queue>
#include <fstream>
using namespace std;
#define maxn 500010

// link-edge 
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

// optimized Bellman-Ford : SPFA
bool spfa(int s,int t) 
{

	// initialization work

	memset(dis,1e9+7,sizeof(dis)); 
	memset(flow,1e9+7,sizeof(flow));
	memset(vis,0,sizeof(vis));
    

	q.push(s);        //start from start point 
	vis[s] = 1;      // visited
	dis[s] = 0;      // distanve = 0
	pre[t] = -1;      
	
	while(!q.empty())
	{
		int now = q.front();
		q.pop();
		vis[now] = 0; 

		for(int i=head[now];i > 0;i=e[i].ne)
		{
			int k =e[i].to;    // adj vetex 

			if(e[i].w != 0 && dis[k] > dis[now]+e[i].co)      // w == 0 -> no edge
			{
				dis[k] = dis[now] + e[i].co; 
				pre[k] = now;  // note down the last vertex
				last[k] = i;  // note down the last edge
				flow[k] = min(flow[now],e[i].w);  //update flow to the min(e[s], ..., e[t])
				
				
				if(!vis[k])
				{
					vis[k] = 1;
					q.push(k);
				}


			}
		}
	}
	return pre[t] != -1;   // if 0, there is no path
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
			e[last[now]].w -= flow[t];  // f(a, b) - bottleneck flow
			e[last[now]^1].w += flow[t]; // f(b, a) + bottleneck flow

			now = pre[now];
		}
	}

	cout << "maxflow " << maxflow << " " << "mincost " << mincost << endl;
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
