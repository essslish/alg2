// rb.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
#include <iostream>

enum Color { RED, BLACK };
using namespace std;

struct rb_node {
    int data;
    Color color;
    rb_node* left, * right, * parent;

    rb_node(int value) : data(value), color(RED), left(nullptr), right(nullptr), parent(nullptr) {}
};

struct rb_tree {
    rb_node* root;

    rb_tree() : root(nullptr) {}

    void insert(int value) {
        rb_node* newNode = new rb_node(value);
        root = bst_ins(root, newNode);
        fix_ins(newNode);
    }

    rb_node* bst_ins(rb_node* root, rb_node* newNode) {
        if (root == nullptr) return newNode;

        if (newNode->data < root->data) {
            root->left = bst_ins(root->left, newNode);
            root->left->parent = root;
        }
        else {
            root->right = bst_ins(root->right, newNode);
            root->right->parent = root;
        }
        return root;
    }

    void fix_ins(rb_node* node) {
        while (node != root && node->parent->color == RED) {
            if (node->parent == node->parent->parent->left) {
                rb_node* uncle = node->parent->parent->right;
                if (uncle && uncle->color == RED) {
                    node->parent->color = BLACK;
                    uncle->color = BLACK;
                    node->parent->parent->color = RED;
                    node = node->parent->parent;
                }
                else {
                    if (node == node->parent->right) {
                        node = node->parent;
                        rot_left(node);
                    }
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    rot_right(node->parent->parent);
                }
            }
            else {
                rb_node* uncle = node->parent->parent->left;
                if (uncle && uncle->color == RED) {
                    node->parent->color = BLACK;
                    uncle->color = BLACK;
                    node->parent->parent->color = RED;
                    node = node->parent->parent;
                }
                else {
                    if (node == node->parent->left) {
                        node = node->parent;
                        rot_right(node);
                    }
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    rot_left(node->parent->parent);
                }
            }
        }
        root->color = BLACK;
    }

    void rot_left(rb_node* node) {
        rb_node* y = node->right;
        node->right = y->left;
        if (y->left != nullptr) y->left->parent = node;

        y->parent = node->parent;
        if (node->parent == nullptr) {
            root = y;
        }
        else if (node == node->parent->left) {
            node->parent->left = y;
        }
        else {
            node->parent->right = y;
        }
        y->left = node;
        node->parent = y;
    }

    void rot_right(rb_node* node) {
        rb_node* y = node->left;
        node->left = y->right;
        if (y->right != nullptr) y->right->parent = node;

        y->parent = node->parent;
        if (node->parent == nullptr) {
            root = y;
        }
        else if (node == node->parent->right) {
            node->parent->right = y;
        }
        else {
            node->parent->left = y;
        }
        y->right = node;
        node->parent = y;
    }

    rb_node* search(rb_node* root, int value) {
        if (root == nullptr || root->data == value) {
            return root;
        }

        if (value < root->data) {
            return search(root->left, value);
        }
        return search(root->right, value);
    }

    bool search_val(int num) {
        return search(root, num) != nullptr;
    }

 
    void in_order() {
        in_order_help(root);
        cout << endl;
    }

    void in_order_help(rb_node* node) {
        if (node == nullptr) return;
        in_order_help(node->left);
        cout << node->data << " ";
        in_order_help(node->right);
    }

    void pre_order(rb_node* node) {
        if (node == nullptr) return;
        cout << node->data << " ";
        pre_order(node->left);
        pre_order(node->right);
    }

    void post_order(rb_node* node) {
        if (node == nullptr) return;
        post_order(node->left);
        post_order(node->right);
        cout << node->data << " ";
    }

    
    void level_order() {
        if (root == nullptr) return;

        rb_node* queue[100];  
        int front = 0;     
        int rear = 0;      

        queue[rear++] = root; 

        while (front < rear) {
            rb_node* node = queue[front++];  
            cout << node->data << " "; 

            if (node->left != nullptr) {
                queue[rear++] = node->left;
            }
            if (node->right != nullptr) {
                queue[rear++] = node->right;
            }
        }
        cout << endl;
    }

    void del_val(int value) {
        rb_node* node_del = search(root, value);
        if (node_del) {
            deleteNode(node_del);
        }
    }

    void deleteNode(rb_node* node) {
        rb_node* y = node, * x;
        Color or_col = y->color;

        if (node->left == nullptr) {
            x = node->right;
            rep(node, node->right);
        }
        else if (node->right == nullptr) {
            x = node->left;
            rep(node, node->left);
        }
        else {
            y = minimum(node->right);
            or_col = y->color;
            x = y->right;
            if (y->parent == node) {
                if (x) x->parent = y;
            }
            else {
                rep(y, y->right);
                y->right = node->right;
                if (y->right) y->right->parent = y;
            }
            rep(node, y);
            y->left = node->left;
            if (y->left) y->left->parent = y;
            y->color = node->color;
        }

        delete node;
        if (or_col == BLACK) {
            if (x != nullptr) {
                fix_del(x);
            }
        }
    }

    void rep(rb_node* u, rb_node* v) {
        if (u->parent == nullptr) {
            root = v;
        }
        else if (u == u->parent->left) {
            u->parent->left = v;
        }
        else {
            u->parent->right = v;
        }
        if (v != nullptr) {
            v->parent = u->parent;
        }
    }

    rb_node* minimum(rb_node* node) {
        while (node->left != nullptr) {
            node = node->left;
        }
        return node;
    }

    void fix_del(rb_node* x) {
        while (x != root && (x == nullptr || x->color == BLACK)) {
            if (x == x->parent->left) {
                rb_node* w = x->parent->right;
                if (w->color == RED) {
                    w->color = BLACK;
                    x->parent->color = RED;
                    rot_left(x->parent);
                    w = x->parent->right;
                }
                if ((w->left == nullptr || w->left->color == BLACK) &&
                    (w->right == nullptr || w->right->color == BLACK)) {
                    w->color = RED;
                    x = x->parent;
                }
                else {
                    if (w->right == nullptr || w->right->color == BLACK) {
                        if (w->left != nullptr) w->left->color = BLACK;
                        w->color = RED;
                        rot_right(w);
                        w = x->parent->right;
                    }
                    w->color = x->parent->color;
                    x->parent->color = BLACK;
                    if (w->right != nullptr) w->right->color = BLACK;
                    rot_left(x->parent);
                    x = root;
                }
            }
            else {
                rb_node* w = x->parent->left;
                if (w->color == RED) {
                    w->color = BLACK;
                    x->parent->color = RED;
                    rot_right(x->parent);
                    w = x->parent->left;
                }
                if ((w->right == nullptr || w->right->color == BLACK) &&
                    (w->left == nullptr || w->left->color == BLACK)) {
                    w->color = RED;
                    x = x->parent;
                }
                else {
                    if (w->left == nullptr || w->left->color == BLACK) {
                        if (w->right != nullptr) w->right->color = BLACK;
                        w->color = RED;
                        rot_left(w);
                        w = x->parent->left;
                    }
                    w->color = x->parent->color;
                    x->parent->color = BLACK;
                    if (w->left != nullptr) w->left->color = BLACK;
                    rot_right(x->parent);
                    x = root;
                }
            }
        }
        if (x != nullptr) x->color = BLACK;
    }
};

int main() {
    setlocale(LC_ALL, "Russian");
    rb_tree tree;

    tree.insert(7);
    tree.insert(3);
    tree.insert(18);
    tree.insert(10);
    tree.insert(22);
    tree.insert(8);
    tree.insert(11);
    tree.insert(26);
    tree.insert(2);
    tree.insert(6);
    tree.insert(13);

    cout << "Центрированный обход: ";
    tree.in_order();

    tree.del_val(18);
    tree.del_val(13);
    tree.del_val(3);
    tree.del_val(8);
    tree.del_val(22);

    cout << "Дерево после удаления 18, 13, 3, 8, 22: ";
    tree.in_order();

    tree.insert(16);
    tree.insert(4);

    cout << "Дерево после вставки 16 и 4: ";
    tree.in_order();

    cout << "Есть ли 13 в дереве?" << (tree.search_val(13) ? " Да" : " Нет") << endl;
    cout << "Есть ли 16 в дереве?" << (tree.search_val(16) ? " Да" : " Нет") << endl;
    cout << "Есть ли 7 в дереве?" << (tree.search_val(7) ? " Да" : " Нет") << endl;
    cout << "Есть ли 100 в дереве?" << (tree.search_val(100) ? " Да" : " Нет") << endl;
    

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
