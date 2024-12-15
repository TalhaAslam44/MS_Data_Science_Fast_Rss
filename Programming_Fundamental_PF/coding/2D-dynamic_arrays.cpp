#include<iostream>
using namespace std;
// M x N matrix
#define M 4
#define N 5

// Dynamically Allocate Memory for 2D Array in c++

int main()
{
    int* A = new int[M * N];
    
    // Assigning value to memory
    for (int i=0 ; i<M; i++)
        for (int j=0 ; j<N;j++)
            *(A + i*N + j) = rand() %100;

    // print the 2D array
    for (int i=0 ; i<M;i++)
    {
        for (int j =0; j<N ; j++)
        cout << *(A + i*N + j) << "";

        cout << endl;

    }
    // dellocate memory
    delete[] A;
    return 0;
}