#include<iostream>
#include<fstream>
#include<map>
#include<vector>
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


template <typename T>
vector<T> &operator +(vector<T> &v1,vector<T> &v2){
    v1.insert(v1.end(),v2.begin(),v2.end());
    return v1;
}



int min(int a, int b){return a > b ? b : a;}

int cost(char a, char b){return Cost[dna_to_id[a]][dna_to_id[b]];}

int find_row(int a1, int b1, int a2, int b2){
    
    // return the row number of the min(f+g)

    // assert a2 > a1, b2 > b1, a2 - a1 > 1

    // cal f(a1, *) (0, 0) -> (a1, i) 
    int *last, *pres;
    int mid = (a1 + a2) >> 1;
    last = new int[b2 + 5];
    pres = new int[b2 + 5];


    for(int i = 0;i < b2 + 5;++i){
        last[i] = 0;
        pres[i] = 0;
    }
    

    for(int i = a1;i <= mid;++i){
        for(int j = b1;j <= b2;++j){
            int k1, k2, k3;
            k1 = last[j - 1] + cost(A[i], B[j]);
            k2 = last[j] + cost('-', A[i]);
            k3 = pres[j - 1] + cost('-', B[j]); 
            pres[j] = min(min(k1, k2), k3);
        }
        for(int m = 0;m < b2 + 5;++m)
            last[m] = pres[m];
    }



    // cal g(a1, *): from (a2, b2) to (mid, *)

    int *last2, *pres2;
    last2 = new int[b2 + 5];
    pres2 = new int[b2 + 5];

    for(int i = 0;i < b2 + 5;++i){
        last2[i] = 0;
        pres2[i] = 0;
    }


    for(int i = a2;i >= mid; --i){
        for(int j = b2;j >= b1; --j){
            int k1, k2, k3;
            k1 = last2[i + 1] + cost(A[i], B[j]);
            k2 = last2[i] + cost('-', A[i]);
            k3 = pres2[j + 1] + cost('-', B[j]);
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
        for(int i = a1;i < a2;++i)
            p.push_back(make_pair(i, b1));
    }
    if(a1 == a2){
        for(int j = b1;j < b2;++j)
            p.push_back(make_pair(a1, j));
    }   
    if(a2 - a1 > 1){
        int min_row = find_row(a1, b1, a2, b2);
        p.push_back(make_pair(min_row, mid));
        p = HischbergAlg(a1, mid, b1, min_row) + p + HischbergAlg(mid, a2, min_row, b2);
    }else{
        // a2 - a1 = 1
        // just dp to find opt path from (a1, b1) to (a2, b2)

        int **dp;
        dp = new int*[b2+5];
        for(int i  = 0;i < b2 + 5;++i)
            dp[i] = new int[2];
        
        




    }



    return p;

}


void WriteDNA(){
    // get the modified dna according the path
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
         A.push_back(c);  
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
         B.push_back(c);  
    }
    cout << "Get DATA of B succeffully---total length: " << B.size() << endl;
    finb.close();

    lena = A.size() - 1; // since "*" is added 
    lenb = B.size() - 1;


}




int main(){
    init();
    HischbergAlg(0, lena, 0, lenb);
    WriteDNA();
    system("pause");
    return 0;
}