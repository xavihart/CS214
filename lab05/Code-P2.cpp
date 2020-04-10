#include<iostream>
#include<fstream>
#include<map>
#include<vector>
#include<cstring>
#include<string>
using namespace std;

// dna string
string A = "*";   // to make A[1] be the first element
string B = "*";   
int lena, lenb;


// map and matrix
map<char, int> dna_to_id;
map<int, char> id_to_dna;
char dna[5] = {'-', 'A', 'T', 'G', 'C'};
char* opti_list;
int Cost[5][5] = {
    {0, 1, 2, 1, 3}, 
    {1, 0, 1, 5, 1},
    {2, 1, 0, 9, 1}, 
    {1, 5, 9, 0, 1}, 
    {3, 1, 1, 1, 0}
};

//ans stack
vector<pair<int, int>> path;
int last[100010];
int pres[100010];
int last2[100010];
int pres2[100010];
int dp[100010][2];
int s[100010][2];




template <typename T>
vector<T> &operator +(vector<T> &v1,vector<T> &v2){
    v1.insert(v1.end(),v2.begin(),v2.end());
    return v1;
}

void show_path(vector<pair<int, int>> p){
    for(int i = 0;i < p.size();++i){
        cout << "(" << p[i].first << "," << p[i].second << ")" ;
    }
    cout << endl;
}


int min(int a, int b){return a > b ? b : a;}

int cost(char a, char b){return Cost[dna_to_id[a]][dna_to_id[b]];}

int find_row(int a1, int b1, int a2, int b2){
    
    // return the row number of the min(f+g)

    // assert a2 > a1, b2 > b1, a2 - a1 > 1

    // cal f(a1, *) (0, 0) -> (a1, i) 
    /*
    int *last, *pres;
    
    last = new int[b2 + 5];
    pres = new int[b2 + 5];
    */


    int mid = (a1 + a2) >> 1;
   


    for(int i = 0;i < b2 + 5;++i){
        last[i] = 0;
        pres[i] = 0;
    }

    for(int i = b1 + 1;i <= b2;++i){
        last[i] = last[i - 1] + Cost[0][B[i] - '0'];
    }
    
    int tmp = 0;
    for(int i = a1 + 1;i <= mid;++i){
        //cout << i << "\n";
        for(int j = b1;j <= b2;++j){
            if(j == b1){
                pres[j] = tmp + Cost[0][A[i] - '0'];
                tmp += Cost[0][A[i] - '0'];
                continue;
            }
            int k1, k2, k3;
            k1 = last[j - 1] + Cost[A[i] - '0'][B[j] - '0'];
            k2 = last[j] + Cost[0][A[i] - '0'];
            k3 = pres[j - 1] + Cost[0][B[j] - '0']; 
            pres[j] = min(min(k1, k2), k3);
        }
        for(int m = 0;m < b2 + 5;++m)
            last[m] = pres[m];
    }



    // cal g(a1, *): from (a2, b2) to (mid, *)
    /*
    int *last2, *pres2;
    last2 = new int[b2 + 5];
    pres2 = new int[b2 + 5];
    */

    

    for(int i = 0;i < b2 + 5;++i){
        last2[i] = 0;
        pres2[i] = 0;
    }

    for(int i = b2 - 1;i >= b1;--i){
        last2[i] = last2[i + 1] + Cost[0][B[i + 1] - '0'];
    }

    

    tmp = 0;
    for(int i = a2 - 1;i >= mid; --i){
        for(int j = b2;j >= b1; --j){

            if(j == b2){
                pres2[j] = tmp + Cost[A[i + 1] - '0'][0];
                tmp += Cost[A[i + 1] - '0'][0];
                continue;
            }

            int k1, k2, k3;
            k1 = last2[j + 1] + Cost[A[i + 1] - '0'][B[j + 1] - '0'];
            k2 = last2[j] + Cost[0][A[i + 1] - '0'];
            k3 = pres2[j + 1] + Cost[0][B[j +1] - '0'];
            pres2[j] = min(min(k1, k2), k3);

        }
        for(int m = 0;m < b2 + 5;++m)
            last2[m] = pres2[m];
    }

    // get minimul row index

    int min_index = b1;

    for(int i = b1;i <= b2;++i){
        if(last[i] + last2[i] < last[min_index] + last2[min_index]){
            min_index = i;
        }
    }


    return min_index;
}


vector<pair<int, int>>  HischbergAlg(int a1, int a2, int b1, int b2){
    vector<pair<int, int>> p;
    int mid = (a1 + a2) >> 1;
   

    if(b1 == b2){
        for(int i = a1;i <= a2;++i)
            p.push_back(make_pair(i, b1));
        //show_path(p);
        return p;
    }
    if(a1 == a2){
        for(int j = b1;j <= b2;++j)
            p.push_back(make_pair(a1, j));
        return p;
    }   



    if(a2 - a1 > 1){
        int min_row = find_row(a1, b1, a2, b2);
        //p.push_back(make_pair(min_row, mid));
        vector<pair<int, int>> left, right;
        left = HischbergAlg(a1, mid, b1, min_row);
        right = HischbergAlg(mid, a2, min_row, b2);
        left.pop_back();
        p = left + right;
    }
    else if(a2 - a1 == 1){
        // a2 - a1 = 1
        // just dp to find opt path from (a1, b1) to (a2, b2)
        /*
        int **dp;
        dp = new int*[b2+5];
        for(int i  = 0;i < b2 + 5;++i)
            dp[i] = new int[2];

        int **s;
        s = new int*[b2+5];
        for(int i  = 0;i < b2 + 5;++i)
            s[i] = new int[2];
            
        for(int i = 0;i < b2 + 5;++i)
            for(int j = 0;j < 3;++j)
                dp[i][j] = 0;

        */

       dp[b1][0] = 0;

        for(int i = b1 + 1;i <= b2;++i){
            dp[i][0] = dp[i - 1][0] +  Cost[0][B[i] - '0'];
            s[i][0] = 1;
        }

        dp[b1][1] = dp[b1][0] + Cost[0][A[a1 + 1] - '0'];
        s[b1][1] = 2;



        for(int i = b1 + 1;i <= b2;++i){
            int k1, k2, k3;
            k3 = dp[i - 1][0] + Cost[B[i] - '0'][A[a1 + 1] - '0'];
            k2 = dp[i][0] + Cost[0][A[a1 + 1] - '0'];
            k1 = dp[i - 1][1] + Cost[0][B[i] - '0'];
            dp[i][1] = min(min(k1, k2), k3);
            if(dp[i][1] == k1){
                s[i][1] = 1;
            }
            else if(dp[i][1] == k2){
                s[i][1] = 2;
            }
            else if(dp[i][1] == k3){
                s[i][1] = 3;
            }
        }

        //cout << dp[0][0] << endl;
        
      

        int a=a2, b=b2;
        
        
       int q = 0;

        while(a != a1 || b != b1){
            switch(s[b][a- a1]){
                case 3:
                    a --;
                    b --;
                    break;    
                case 2:
                    a --;
                    break;    
                case 1:
                    b--;
                    break;
                default: break;

            };
            p.insert(p.begin(), make_pair(a, b));
        }

        p.insert(p.end(), make_pair(a2, b2));


    }

    else{
        cout << "assert a1, a2!!!\n";
        system("pause");
    }

    //std::cout << a1 << b1 << a2 << b2 << endl;
    //show_path(p);
    return p;

}


void WriteDNA(){
    // get the modified dna according the path
    pair<int, int> pre = make_pair(0, 0);
    int pa=1, pb=1;

    int pena=0;
    for(int i = 1; i < path.size();++i){
        if(path[i].first == pre.first){
            pena += Cost[0][B[path[i].second] - '0'];
        }
        else if(path[i].second == pre.second){
            pena += Cost[0][A[path[i].first]- '0'];
        }
        else {
            pena += Cost[A[path[i].first]- '0'][B[path[i].second]- '0'];
        }
        pre = make_pair(path[i].first, path[i].second);
    }

    pre = make_pair(0, 0);


    for(int i = 1;i < path.size();++i){
        if(path[i].first == pre.first){
            A.insert(pa, 1, '0');
        }
        else if(path[i].second == pre.second){
            B.insert(pb, 1, '0');
        }
       
            pa ++;
            pb ++;
        
        pre = make_pair(path[i].first, path[i].second);
    }
    
    
    A.erase(0, 1);
    B.erase(0, 1);
    //show_path(path);
    int pen = 0;
    for(int i = 0;i < A.size();++i){
        pen += Cost[A[i] - '0'][B[i] - '0'];
    }

    for(int i = 0;i < A.size();++i){
        A[i] = id_to_dna[A[i] - '0'];
    }

    for(int i = 0;i < B.size();++i){
        B[i] = id_to_dna[B[i] - '0'];
    }

   //std::cout << A << endl;
   //std::cout << B << endl;


   ofstream oa("./result2/resulta.txt"), ob("./result2/resultb.txt");

   if(!oa || !ob){
       cout << "result file open failed!!!\n";
   }

   oa << A;
   ob << B;

   oa.close();
   ob.close();

   cout << pen << endl;


   //show_path(path);

}


void init(){

    // init map
    for(int i = 0;i < 5;++i){
        dna_to_id[dna[i]] = i;
        id_to_dna[i] = dna[i];
    }



    // read data in a
    fstream fina("Data-P2a.txt");
    if(!fina){
        cerr << "cannoot open file Data-P2a!" << endl;
    }
    char c;
    while(fina.get(c)){
         if(c == '\n') continue;

         switch(c){
             case 'A':A.push_back('1');break;  
             case 'T':A.push_back('2');break;  
             case 'G':A.push_back('3');break;  
             case 'C':A.push_back('4');break;  
         }
   
    }
    cout << "Get DATA of A succeffully---total length: " << A.size() << endl;
    fina.close();
    
    // read data in b
    fstream finb("Data-P2b.txt");
    if(!finb){
        cerr << "cannoot open file Data-P2b!" << endl;
    }
    
    while(finb.get(c)){
         if(c == '\n') continue;
         switch(c){
             case 'A':B.push_back('1');break;  
             case 'T':B.push_back('2');break;  
             case 'G':B.push_back('3');break;  
             case 'C':B.push_back('4');break;  
         } 
    }
    std::cout << "Get DATA of B succeffully---total length: " << B.size() << endl;
    finb.close();

    lena = A.size() - 1; // since "*" is added 
    lenb = B.size() - 1;


}




int main(){
    init();
    path = HischbergAlg(0, lena, 0, lenb);
    std::cout << "path finded---\n";
    WriteDNA();
    std::cout << "Done ----\n";
    system("pause");
    return 0;
}