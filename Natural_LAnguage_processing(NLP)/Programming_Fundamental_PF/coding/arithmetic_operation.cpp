#include<iostream>  
using namespace std;

int main()
{
    int a = 4;
    int b = 5;
    int sum = a +b;
    int remainder = a % b;
    int y=5;
    int x=6;
    x++;
    y=x++; //(y=5,x=6)
    x--;
    ++x;
    --x;
    cout << "Sum is " << x << endl;
    cout << "Remainder is " << y << endl;
}