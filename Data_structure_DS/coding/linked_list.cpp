#include<iostream>
using namespace std;

// structure
struct Node{
    int data;
    Node* next;
};

// Initailization
Node* head = nullptr;

//function
void insertatfront (int data){
    Node* temp1 = new Node;
    temp1 -> data = data;
    temp1 -> next = nullptr;

    if (head == nullptr){  // checking if list is empty
        head =temp1;
    }
    else {
        temp1 -> next = head;
        head = temp1;
    }
}

// function to print the linked list
void printlist(){
Node* current = head;
while (current != nullptr){
    cout << current -> data << "";
    current = current ->next;

}
}

// main function

int main(){
    insertatfront(30);
    insertatfront(20);
    insertatfront(10);

    cout << "Linked list: ";
    printlist();


}