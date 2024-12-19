#include <iostream>
using namespace std;

// structure
struct Node{
    int data;
    Node* next;
};

// initialization
Node* head = nullptr;

// function to add node at the end
void insertatend(int data){
    Node* temp1 = new Node;
    temp1 -> data = data;
    temp1 -> next =  nullptr;

    if (head ==  nullptr){
    head = temp1;
    }
    else {
        Node* current = head;
        while (current -> next = nullptr){
            current = current -> next;
        }
        current -> next = temp1;
    }
}

// function to print list
void printlist() {
    Node* current = head;
    while (current != nullptr) {
        cout << current -> data << "";
        current = current -> next ;
        }
        cout << "nullptr";

}

int main(){
    insertatend(10);
    insertatend(20);
    insertatend(30);

    cout << "Linked lists: ";
    printlist();
    return 0;
}