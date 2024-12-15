#include<iostream>
using namespace std;
int main()
{
    int v1 = 55;
    int* p1 = &v1;
    int* p2;
    p2=p1;
    cout << *p2 << endl;
    cout << *p1 << endl;
}