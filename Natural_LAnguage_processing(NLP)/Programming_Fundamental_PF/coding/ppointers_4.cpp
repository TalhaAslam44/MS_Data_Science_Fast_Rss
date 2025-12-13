#include<iostream>
using namespace std;    
int main()
{
    int i = 2;
    int j= 3;
    int* ptr;
    ptr = &i;
    *ptr =3;
    ptr = &j;
    *ptr = 4;
    cout<< i << "" << j<< endl;



}