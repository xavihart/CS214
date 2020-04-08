#include<iostream>
#include<fstream>
#include<map>
#include<vector>
#include<cstring>
#include<string>
using namespace std;
int Cost[5][5] = {
    {0, 1, 2, 1, 3}, 
    {1, 0, 1, 5, 1},
    {2, 1, 0, 9, 1}, 
    {1, 5, 9, 0, 1}, 
    {3, 1, 1, 1, 0}
};
int main(){
    fstream a("./result2/resulta.txt"), b("./result2/resultb.txt");
    string A, B;
    char c;
     while(a.get(c)){
         if(c == '\n') continue;

         switch(c){
             case 'A':A.push_back('1');break;  
             case 'T':A.push_back('2');break;  
             case 'G':A.push_back('3');break;  
             case 'C':A.push_back('4');break;  
             case '-':A.push_back('0');break;
         }
   
    }

    while(b.get(c)){
         if(c == '\n') continue;
         switch(c){
             case 'A':B.push_back('1');break;  
             case 'T':B.push_back('2');break;  
             case 'G':B.push_back('3');break;  
             case 'C':B.push_back('4');break;  
             case '-':B.push_back('0');break;
         } 
    }

    cout << "len of A:" << A.size() << endl;
    cout << "len of B:" << B.size() << endl;
    
    int p = 0;
    int same = 0;
    for(int i = 0;i < A.size();++i){
        p += Cost[A[i] - '0'][B[i] - '0'];
        if(A[i] == B[i]) same ++;
    }

    cout << "penalty:" << p << endl;
    cout << "same:" << same << endl;
    system("pause");
    
    return 0;
}
