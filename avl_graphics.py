import time
import random
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def rotateRight(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        return x

    def rotateLeft(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        balance = self.getBalance(node)

        # Балансировка AVL-дерева
        if balance > 1 and key < node.left.key:
            return self.rotateRight(node)
        if balance < -1 and key > node.right.key:
            return self.rotateLeft(node)
        if balance > 1 and key > node.left.key:
            node.left = self.rotateLeft(node.left)
            return self.rotateRight(node)
        if balance < -1 and key < node.right.key:
            node.right = self.rotateRight(node.right)
            return self.rotateLeft(node)

        return node

    def deleteNode(self, key):
        self.root = self._deleteNode(self.root, key)

    def _deleteNode(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._deleteNode(node.left, key)
        elif key > node.key:
            node.right = self._deleteNode(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                del node
                return temp
            elif node.right is None:
                temp = node.left
                del node
                return temp
            temp = self.findMin(node.right)
            node.key = temp.key
            node.right = self._deleteNode(node.right, temp.key)

        if not node:
            return node

        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        balance = self.getBalance(node)

        # Балансировка AVL-дерева после удаления
        if balance > 1 and self.getBalance(node.left) >= 0:
            return self.rotateRight(node)
        if balance > 1 and self.getBalance(node.left) < 0:
            node.left = self.rotateLeft(node.left)
            return self.rotateRight(node)
        if balance < -1 and self.getBalance(node.right) <= 0:
            return self.rotateLeft(node)
        if balance < -1 and self.getBalance(node.right) > 0:
            node.right = self.rotateRight(node.right)
            return self.rotateLeft(node)

        return node

    def findMin(self, node):
        if node is None:
            return None
        while node.left:
            node = node.left
        return node

    def getHeightTree(self):
        return self.getHeight(self.root)

numbers = list(range(1000000))
random.shuffle(numbers)

data = []
tree = AVLTree()
for i, num in enumerate(numbers):
    start_insert = time.perf_counter_ns()
    tree.insert(num)
    end_insert = time.perf_counter_ns()

    if (i + 1) % 16000 == 0:
        start_delete = time.perf_counter_ns()
        if i > 0:
            tree.deleteNode(numbers[i // 2])
        end_delete = time.perf_counter_ns()
        data.append((i + 1, end_insert - start_insert, end_delete - start_delete, tree.getHeightTree()))

sizes, insert_times, delete_times, heights = zip(*data)

coeffs_insert = np.polyfit(np.log(sizes), insert_times, 1)
coeffs_delete = np.polyfit(np.log(sizes), delete_times, 1)
coeffs_height = np.polyfit(np.log(sizes), heights, 1)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.scatter(sizes, insert_times, s=10, label="Данные")
plt.plot(sizes, coeffs_insert[0] * np.log(sizes) + coeffs_insert[1], color='red', label=f"Аппроксимация: {coeffs_insert[0]:.2f}log(x) + {coeffs_insert[1]:.2f}")
plt.xlabel("Количество элементов")
plt.ylabel("Время вставки (нс)")
plt.title("Зависимость времени вставки")
plt.legend()

plt.subplot(1, 3, 2)
plt.scatter(sizes, delete_times, s=10, label="Данные")
plt.plot(sizes, coeffs_delete[0] * np.log(sizes) + coeffs_delete[1], color='red', label=f"Аппроксимация: {coeffs_delete[0]:.2f}log(x) + {coeffs_delete[1]:.2f}")
plt.xlabel("Количество элементов")
plt.ylabel("Время удаления (нс)")
plt.title("Зависимость времени удаления")
plt.legend()

plt.subplot(1, 3, 3)
plt.scatter(sizes, heights, s=10, label="Данные")
plt.plot(sizes, coeffs_height[0] * np.log(sizes) + coeffs_height[1], color='red', label=f"Аппроксимация: {coeffs_height[0]:.2f}log(x) + {coeffs_height[1]:.2f}")
plt.xlabel("Количество элементов")
plt.ylabel("Высота")
plt.title("Зависимость высоты")
plt.legend()

plt.tight_layout()
plt.show()
