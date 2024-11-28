// bst.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
using namespace std;

struct BST_Node {
    int data;
    BST_Node* left;
    BST_Node* right;
};

BST_Node* new_one(int data) {
    BST_Node* newNode = new BST_Node();
    newNode->data = data;
    newNode->left = newNode->right = nullptr;
    return newNode;
}

BST_Node* insert_node(BST_Node* root, int data) {
    if (root == nullptr) {
        return new_one(data);
    }

    if (data < root->data) {
        root->left = insert_node(root->left, data);

    }

    else if (data > root->data) {
        root->right = insert_node(root->right, data);
    }

    return root;
}

void in_order(BST_Node* root) {
    if (root != nullptr) {
        in_order(root->left);
        cout << root->data << " ";
        in_order(root->right);
    }
}

BST_Node* search_node(BST_Node* root, int key) {
    if (root == nullptr || root->data == key) {
        return root;
    }

    if (root->data < key) {
        return search_node(root->right, key);
    }

    return search_node(root->left, key);
}

BST_Node* min_val(BST_Node* node) {
    BST_Node* cur = node;
    while (cur && cur->left != nullptr) {
        cur = cur->left;
    }
    return cur;
}

BST_Node* delete_n(BST_Node* root, int data) {
    if (root == nullptr)
        return root;

    if (data < root->data) {
        root->left = delete_n(root->left, data);
    }

    else if (data > root->data) {
        root->right = delete_n(root->right, data);
    }

    else {
        if (root->left == nullptr) {
            BST_Node* temp = root->right;
            delete root;
            return temp;
        }

        else if (root->right == nullptr) {
            BST_Node* temp = root->right;
            delete root;
            return temp;
        }

        BST_Node* temp = min_val(root->right);
        root->data = temp->data;
        root->right = delete_n(root->right, temp->data);
    }
    return root;
}

int main()
{
    setlocale(LC_ALL, "Russian");
    BST_Node* root = nullptr;

    root = insert_node(root, 44);
    root = insert_node(root, 33);
    root = insert_node(root, 10);
    root = insert_node(root, 81);
    root = insert_node(root, 4);
    root = insert_node(root, 16);
    root = insert_node(root, 3);
    root = insert_node(root, 55);

    cout << "Дерево по порядку:";
    in_order(root);
    cout << endl;

    root = delete_n(root, 3);
    cout << "После удаления 3: ";
    in_order(root);
    cout << endl;

    root = insert_node(root, 0);
    cout << "После вставки 0: ";
    in_order(root);
    cout << endl;

    BST_Node* f = search_node(root, 0);
    if (f != nullptr) {
        cout << "0 найдено";
    }
    else {
        cout << "0 нет";
    }

    return 0;

}

// Запуск программы: CTRL+F5 или меню "Отладка" > "Запуск без отладки"
// Отладка программы: F5 или меню "Отладка" > "Запустить отладку"

// Советы по началу работы 
//   1. В окне обозревателя решений можно добавлять файлы и управлять ими.
//   2. В окне Team Explorer можно подключиться к системе управления версиями.
//   3. В окне "Выходные данные" можно просматривать выходные данные сборки и другие сообщения.
//   4. В окне "Список ошибок" можно просматривать ошибки.
//   5. Последовательно выберите пункты меню "Проект" > "Добавить новый элемент", чтобы создать файлы кода, или "Проект" > "Добавить существующий элемент", чтобы добавить в проект существующие файлы кода.
//   6. Чтобы снова открыть этот проект позже, выберите пункты меню "Файл" > "Открыть" > "Проект" и выберите SLN-файл.
