#include<iostream>
using namespace std;

template<class elemtype>
class list
{
public:
    virtual void clear()=0;
    virtual int length()const=0;
    virtual void insert(int i,const elemtype&x)=0;
    virtual void remove(int i)=0;
    virtual int search(const elemtype&x)const=0;
    virtual elemtype visit(int i)const=0;
    virtual void traverse()const=0;
    virtual ~list(){};
};

template<class elemtype>
class slinklist:public list<elemtype>
{
private:
    struct node{
    elemtype data;
       node *next;
       node(const elemtype&x,node *n=NULL)
       {
           data=x;next=n;;}
           node():next(NULL){}
           ~node(){}
};


   node *head;
   int currentlength;
   node *move(int i)const;
public:
    slinklist();
    void clear();
    ~slinklist(){clear();delete head;}
    void insert(int i,const elemtype&x);
    node *seqsearch(node *head,const elemtype x);
};

template<class elemtype>
slinklist<elemtype>::slinklist()
{
    head=new node;
    currentlength=0;
}

template<class elemtype>
void slinklist<elemtype>::insert(int i,const elemtype&x)
{
    node *pos;
    pos=move(i-1);
    pos->next=new node(x,pos->next);
    ++currentlength;
}
template<class elemtype>
void slinklist<elemtype>::clear()
{
    node*p=head->next,*q;
    head->next=NULL;
    while(p!=NULL){q=p->next;
    delete p;p=q;}
    currentlength=0;
}

//链接实现
template<class elemtype>
 slinklist<elemtype>::node * slinklist<elemtype>::seqsearch(node *head,elemtype x)
{
    node *p=head;
    while(p!=NULL&&p->data!=x)  {p=p->next;}
    if(p==NULL||p->data!=x) return NULL;
       else  return p;
}
