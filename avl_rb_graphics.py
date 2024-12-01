import time
import matplotlib.pyplot as plt
import numpy as np

#AVL Tree
class NodeAVL:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return NodeAVL(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        node.height = 1 + max(self._getHeight(node.left), self._getHeight(node.right))
        balance = self._getBalance(node)
        if balance > 1 and key < node.left.key:
            return self._rightRotate(node)
        if balance < -1 and key > node.right.key:
            return self._leftRotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self._leftRotate(node.left)
            return self._rightRotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rightRotate(node.right)
            return self._leftRotate(node)
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        elif key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                return temp
            elif node.right is None:
                temp = node.left
                return temp
            temp = self._minValueNode(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        if node is None:
            return node
        node.height = 1 + max(self._getHeight(node.left), self._getHeight(node.right))
        balance = self._getBalance(node)
        if balance > 1 and self._getBalance(node.left) >= 0:
            return self._rightRotate(node)
        if balance > 1 and self._getBalance(node.left) < 0:
            node.left = self._leftRotate(node.left)
            return self._rightRotate(node)
        if balance < -1 and self._getBalance(node.right) <= 0:
            return self._leftRotate(node)
        if balance < -1 and self._getBalance(node.right) > 0:
            node.right = self._rightRotate(node.right)
            return self._leftRotate(node)
        return node

    def _minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _getHeight(self, node):
        if not node:
            return 0
        return node.height

    def _getBalance(self, node):
        if not node:
            return 0
        return self._getHeight(node.left) - self._getHeight(node.right)

    def _rightRotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._getHeight(y.left), self._getHeight(y.right))
        x.height = 1 + max(self._getHeight(x.left), self._getHeight(x.right))
        return x

    def _leftRotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._getHeight(x.left), self._getHeight(x.right))
        y.height = 1 + max(self._getHeight(y.left), self._getHeight(y.right))
        return y

    def height(self):
        return self._getHeight(self.root)



#Red-Black Tree
class NodeRB:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = 1 #1-red, 0-black

class RedBlackTree:
    def __init__(self):
        self.nil = NodeRB(0)
        self.nil.color = 0
        self.root = self.nil

    def insert(self, key):
        node = NodeRB(key)
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y == self.nil:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        node.left = self.nil
        node.right = self.nil
        self._insertFixup(node)

    def _insertFixup(self, node):
        while node.parent and node.parent.color == 1:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 1:
                    node.parent.color = 0
                    uncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._leftRotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self._rightRotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 1:
                    node.parent.color = 0
                    uncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rightRotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self._leftRotate(node.parent.parent)
        self.root.color = 0

    def delete(self, key):
        z = self._search(self.root, key)
        if z == self.nil:
            return
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self._deleteFixup(x)

    def _deleteFixup(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self._leftRotate(x.parent)
                    w = x.parent.right
                if w.left.color == 0 and w.right.color == 0:
                    w.color = 1
                    x = x.parent
                else:
                    if w.right.color == 0:
                        w.left.color = 0
                        w.color = 1
                        self._rightRotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.right.color = 0
                    self._leftRotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self._rightRotate(x.parent)
                    w = x.parent.left
                if w.right.color == 0 and w.left.color == 0:
                    w.color = 1
                    x = x.parent
                else:
                    if w.left.color == 0:
                        w.right.color = 0
                        w.color = 1
                        self._leftRotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.left.color = 0
                    self._rightRotate(x.parent)
                    x = self.root
        x.color = 0

    def _transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    def _search(self, node, key):
        if node == self.nil or key == node.key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node == self.nil:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def _leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y


def main():
    num_elements = 1000000
    numbers = list(range(num_elements))
    rb_tree = RedBlackTree()
    avl_tree = AVLTree()

    rb_data = []
    avl_data = []

    for i, num in enumerate(numbers):
        start_time = time.perf_counter_ns()
        rb_tree.insert(num)
        end_time = time.perf_counter_ns()
        rb_insertion_time = end_time - start_time

        start_time = time.perf_counter_ns()
        avl_tree.insert(num)
        end_time = time.perf_counter_ns()
        avl_insertion_time = end_time - start_time

        if (i + 1) % 16000 == 0:
            start_delete = time.perf_counter_ns()
            if i > 0:
                rb_tree.delete(numbers[i // 2])
            end_delete = time.perf_counter_ns()
            rb_deletion_time = end_delete - start_delete

            start_delete = time.perf_counter_ns()
            if i > 0:
                avl_tree.delete(numbers[i // 2])
            end_delete = time.perf_counter_ns()
            avl_deletion_time = end_delete - start_delete

            rb_height = rb_tree.height()
            avl_height = avl_tree.height()

            rb_data.append((i + 1, rb_insertion_time, rb_deletion_time, rb_height))
            avl_data.append((i + 1, avl_insertion_time, avl_deletion_time, avl_height))

    x_rb, rb_insert_times, rb_delete_times, rb_heights = zip(*rb_data)
    x_avl, avl_insert_times, avl_delete_times, avl_heights = zip(*avl_data)

    coeffs_rb_insert = np.polyfit(np.log(x_rb), rb_insert_times, 1)
    coeffs_avl_insert = np.polyfit(np.log(x_avl), avl_insert_times, 1)
    coeffs_rb_delete = np.polyfit(np.log(x_rb), rb_delete_times, 1)
    coeffs_avl_delete = np.polyfit(np.log(x_avl), avl_delete_times, 1)
    coeffs_rb_height = np.polyfit(np.log(x_rb), rb_heights, 1)
    coeffs_avl_height = np.polyfit(np.log(x_avl), avl_heights, 1)


    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.scatter(x_rb, rb_insert_times, s=10)
    plt.plot(x_rb, coeffs_rb_insert[0] * np.log(x_rb) + coeffs_rb_insert[1], color='red', label=f"RB: y = {coeffs_rb_insert[0]:.2f}log(x) + {coeffs_rb_insert[1]:.2f}")
    plt.scatter(x_avl, avl_insert_times, s=10)
    plt.plot(x_avl, coeffs_avl_insert[0] * np.log(x_avl) + coeffs_avl_insert[1], color='green', label=f"AVL: y = {coeffs_avl_insert[0]:.2f}log(x) + {coeffs_avl_insert[1]:.2f}")
    plt.xlabel("Количество элементов")
    plt.ylabel("Время вставки (нс)")
    plt.title("Сравнение времени вставки")
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.scatter(x_rb, rb_delete_times, s=10)
    plt.plot(x_rb, coeffs_rb_delete[0] * np.log(x_rb) + coeffs_rb_delete[1], color='red', label=f"RB: y = {coeffs_rb_delete[0]:.2f}log(x) + {coeffs_rb_delete[1]:.2f}")
    plt.scatter(x_avl, avl_delete_times, s=10)
    plt.plot(x_avl, coeffs_avl_delete[0] * np.log(x_avl) + coeffs_avl_delete[1], color='green', label=f"AVL: y = {coeffs_avl_delete[0]:.2f}log(x) + {coeffs_avl_delete[1]:.2f}")
    plt.xlabel("Количество элементов")
    plt.ylabel("Время удаления (нс)")
    plt.title("Сравнение времени удаления")
    plt.legend()
    
    plt.subplot(2, 2, 3)
    plt.scatter(x_rb, rb_heights, s=10)
    plt.plot(x_rb, coeffs_rb_height[0] * np.log(x_rb) + coeffs_rb_height[1], color='red', label=f"RB: y = {coeffs_rb_height[0]:.2f}log(x) + {coeffs_rb_height[1]:.2f}")
    plt.scatter(x_avl, avl_heights, s=10)
    plt.plot(x_avl, coeffs_avl_height[0] * np.log(x_avl) + coeffs_avl_height[1], color='green', label=f"AVL: y = {coeffs_avl_height[0]:.2f}log(x) + {coeffs_avl_height[1]:.2f}")
    plt.xlabel("Количество элементов")
    plt.ylabel("Высота")
    plt.title("Сравнение высот")
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
