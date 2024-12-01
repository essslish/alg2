void pre_order(BST_Node* node) { //вместо BST_Node* заменять на  AVL_Node*, реализация обходов для RB tree в файле rb.cpp
    if (node) {
        cout << node->data << " ";
        pre_order(node->left);
        pre_order(node->right);
    }
    else { return; }
}

void post_order(BST_Node* node) {
    if (node) {
        post_order(node->left);
        post_order(node->right);
        cout << node->data << " ";
    }
    else { return; }
}

#define MAX_Q_SIZE 100

struct qu {
    BST_Node* items[MAX_Q_SIZE];
    int front;
    int rear;

    qu() :front(0), rear(0) {}
    bool is_empty() {
        return front == rear;
    }

    void en_qu(BST_Node* node) {
        if (rear >= MAX_Q_SIZE) {
            cout << "Очередь полная";
            return;
        }
        items[rear++] = node;
    }

    BST_Node* de_qu() {
        if (is_empty()) {
            return nullptr;
        }
        return items[front++];
    }
};

void level_order(BST_Node* root) {
    if (!root) return;

    qu que;
    que.en_qu(root);

    while (!que.is_empty()) {
        BST_Node* cur = que.de_qu();
        cout << cur->data << " ";

        if (cur->left) que.en_qu(cur->left);
        if (cur->right) que.en_qu(cur->right);
    }
}

void free_tree(BST_Node* tree) {
    if (tree != NULL) {
        free_tree(tree->left);
        free_tree(tree->right);
        delete tree;
    }
}
