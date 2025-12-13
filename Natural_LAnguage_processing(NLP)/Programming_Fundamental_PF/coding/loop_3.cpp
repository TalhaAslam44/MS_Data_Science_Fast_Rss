#include<iostream>
using namespace std;

int main() {
    int numbers[5] = {1, 2, 3, 4, 5};
    int i = 0;

    while (i < 5) {
        cout << "i = " << i << ", numbers[i] = " << numbers[i] << " ";
        i++;
    }

    return 0;
}
