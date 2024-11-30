import time
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = "red"


class RedBlackTree:
    def __init__(self):
        self.nil = Node(0)
        self.nil.color = "black"
        self.root = self.nil

    def insert(self, key):
        z = Node(key)
        z.left = self.nil
        z.right = self.nil
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.parent.color == "red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    self._left_rotate(z.parent.parent)
        self.root.color = "black"

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
        if y_original_color == "black":
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "black" and w.right.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.right.color == "black":
                        w.left.color = "black"
                        w.color = "red"
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.right.color = "black"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "black" and w.left.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.left.color == "black":
                        w.right.color = "black"
                        w.color = "red"
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.left.color = "black"
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = "black"

    def _transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def _search(self, node, key):
        if node == self.nil or key == node.key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node == self.nil:
            return 0
        else:
            return 1 + max(self._height(node.left), self._height(node.right))

    def _left_rotate(self, x):
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

    def _right_rotate(self, x):
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
    tree = RedBlackTree()
    measurements = []

    for i, num in enumerate(numbers):
        start_time = time.perf_counter_ns()
        tree.insert(num)
        end_time = time.perf_counter_ns()
        insertion_time = end_time - start_time

        if (i + 1) % 16000 == 0:
            start_delete = time.perf_counter_ns()
            if i > 0: 
                tree.delete(numbers[i // 2]) 
            end_delete = time.perf_counter_ns()
            deletion_time = end_delete - start_delete
            height = tree.height()
            measurements.append((i + 1, insertion_time, deletion_time, height))

    x, insertion_times, deletion_times, heights = zip(*measurements)

    
    coeffs_insert = np.polyfit(np.log(x), insertion_times, 1)
    coeffs_delete = np.polyfit(np.log(x), deletion_times, 1)
    coeffs_height = np.polyfit(np.log(x), heights, 1)


    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.scatter(x, insertion_times, s=10, label="Данные")
    plt.plot(x, coeffs_insert[0] * np.log(x) + coeffs_insert[1], color='red', label=f"Аппроксимация: y = {coeffs_insert[0]:.2f}log(x) + {coeffs_insert[1]:.2f}")
    plt.xlabel("Количество элементов")
    plt.ylabel("Время вставки (нс)")
    plt.title("Зависимость времени вставки")
    plt.legend()


    plt.subplot(1, 3, 2)
    plt.scatter(x, deletion_times, s=10, label="Данные")
    plt.plot(x, coeffs_delete[0] * np.log(x) + coeffs_delete[1], color='red', label=f"Аппроксимация: y = {coeffs_delete[0]:.2f}log(x) + {coeffs_delete[1]:.2f}")
    plt.xlabel("Количество элементов")
    plt.ylabel("Время удаления (нс)")
    plt.title("Зависимость времени удаления")
    plt.legend()

    plt.subplot(1, 3, 3)
    plt.scatter(x, heights, s=10, label="Данные")
    plt.plot(x, coeffs_height[0] * np.log(x) + coeffs_height[1], color='red', label=f"Аппроксимация: y = {coeffs_height[0]:.2f}log(x) + {coeffs_height[1]:.2f}")
    plt.xlabel("Количество элементов")
    plt.ylabel("Высота")
    plt.title("Зависимость высоты")
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
