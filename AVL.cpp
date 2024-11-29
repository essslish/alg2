// AVL.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
using namespace std;

struct AVL_Node {
    int key;
    size_t height;
    AVL_Node* left;
    AVL_Node* right;
    AVL_Node(int k) { key = k; left = right = nullptr; height = 1; }
};

size_t height(AVL_Node* p) {
    return p ? p->height : 0;
}

int balance_factor(AVL_Node* p) {
    return height(p->right) - height(p->left);
}

void fix_height(AVL_Node* p) {
    size_t h_left = height(p->left);
    size_t h_right = height(p->right);
    p->height = (h_left > h_right ? h_left : h_right) + 1;
}

AVL_Node* rotate_left(AVL_Node* q) {
    AVL_Node* p = q->right;
    q->right = p->left;
    p->left = q;
    fix_height(q);
    fix_height(p);
    return p;
}

AVL_Node* rotate_right(AVL_Node* p) {
    AVL_Node* q = p->left;
    p->left = q->right;
    q->right = p;
    fix_height(p);
    fix_height(q);
    return q;
}

AVL_Node* balance(AVL_Node* p) {
    fix_height(p);
    if (balance_factor(p) == 2) {
        if (balance_factor(p->right) < 0)
            p->right = rotate_right(p->right);
        return rotate_left(p);
    }
    if (balance_factor(p) == -2) {
        if (balance_factor(p->left) > 0)
            p->left = rotate_left(p->left);
        return rotate_right(p);
    }
    return p;  
}

AVL_Node* insert(AVL_Node* p, int k) {
    if (p == nullptr) return new AVL_Node(k);
    if (k < p->key) {
        p->left = insert(p->left, k);
    }
    else {
        p->right = insert(p->right, k);
    }
    return balance(p);
}

AVL_Node* find_min(AVL_Node* p) {
    return p->left ? find_min(p->left) : p;
}

AVL_Node* remove_min(AVL_Node* p) {
    if (p->left == nullptr)
        return p->right;
    p->left = remove_min(p->left);
    return balance(p);
}

AVL_Node* remove(AVL_Node* p, int k) {
    if (p == nullptr) return 0;
    if (k < p->key) {
        p->left = remove(p->left, k);
    }
    else if (k > p->key) {
        p->right = remove(p->right, k);
    }
    else {
        AVL_Node* left = p->left;
        AVL_Node* right = p->right;
        delete p;
        if (right == nullptr) return left;
        AVL_Node* min = find_min(right);
        min->right = remove_min(right);
        min->left = left;
        return balance(min);
    }
    return balance(p);
}

void in_order(AVL_Node* p) {
    if (p != nullptr) {
        in_order(p->left);
        cout << p->key << " ";
        in_order(p->right);
    }
}

bool search(AVL_Node* p, int key) {
    if (p == nullptr) return false;
    if (key == p->key) return true;
    if (key < p->key) return search(p->left, key);
    return search(p->right, key);
}

int main()
{
    setlocale(LC_ALL, "Russian");
    AVL_Node* root = nullptr;

    root = insert(root, 44);
    root = insert(root, 33);
    root = insert(root, 10);
    root = insert(root, 81);
    root = insert(root, 4);
    root = insert(root, 16);
    root = insert(root, 3);
    root = insert(root, 55);

    cout << "Дерево по порядку:";
    in_order(root);
    cout << endl;

    root = remove(root, 3);
    cout << "После удаления 3: ";
    in_order(root);
    cout << endl;

    root = insert(root, 0);
    cout << "После вставки 0: ";
    in_order(root);
    cout << endl;

    cout << "Есть ли 0 в дереве?" << (search(root, 0) ? " Да" : " Нет") << endl;
    cout << "Есть ли 3 в дереве?" << (search(root, 3) ? " Да" : " Нет") << endl;

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
