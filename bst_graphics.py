import time
import random
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert(root, data):
    if root is None:
        return Node(data)
    if data < root.data:
        root.left = insert(root.left, data)
    else:
        root.right = insert(root.right, data)
    return root

def deleteNode(root, key):
    if root is None:
        return root
    if key < root.data:
        root.left = deleteNode(root.left, key)
    elif key > root.data:
        root.right = deleteNode(root.right, key)
    else:
        if root.left is None:
            temp = root.right
            del root
            return temp
        elif root.right is None:
            temp = root.left
            del root
            return temp
        temp = minValueNode(root.right)
        root.data = temp.data
        root.right = deleteNode(root.right, temp.data)
    return root

def minValueNode(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def height(node):
    if node is None:
        return 0
    else:
        lheight = height(node.left)
        rheight = height(node.right)
        return max(lheight, rheight) + 1

numbers = list(range(1000000))
random.shuffle(numbers)

data = []
root = None
for i, num in enumerate(numbers):
    start_insert = time.perf_counter_ns()
    root = insert(root, num)
    end_insert = time.perf_counter_ns()

    if (i + 1) % 16000 == 0:
        start_delete = time.perf_counter_ns()
        if i > 0: 
          root = deleteNode(root, numbers[i // 2])
        end_delete = time.perf_counter_ns()
        data.append((i + 1, end_insert - start_insert, end_delete - start_delete, height(root)))

sizes, insert_times, delete_times, heights = zip(*data)

coeffs_insert = np.polyfit(np.log(sizes), insert_times, 1)
coeffs_delete = np.polyfit(np.log(sizes), delete_times, 1)
coeffs_height = np.polyfit(np.log(sizes), heights, 1)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.scatter(sizes, insert_times, s=10)
plt.plot(sizes, coeffs_insert[0] * np.log(sizes) + coeffs_insert[1], color='red', label=f"Аппроксимация: {coeffs_insert[0]:.2f}log(x) + {coeffs_insert[1]:.2f}")
plt.xlabel("Количество элементов")
plt.ylabel("Время вставки (нс)")
plt.title("Зависимость времени вставки")

plt.subplot(1, 3, 2)
plt.scatter(sizes, delete_times, s=10)
plt.plot(sizes, coeffs_delete[0] * np.log(sizes) + coeffs_delete[1], color='red', label=f"Аппроксимация: {coeffs_delete[0]:.2f}log(x) + {coeffs_delete[1]:.2f}")
plt.xlabel("Количество элементов")
plt.ylabel("Время удаления (нс)")
plt.title("Зависимость времени удаления")

plt.subplot(1, 3, 3)
plt.scatter(sizes, heights, s=10)
plt.plot(sizes, coeffs_height[0] * np.log(sizes) + coeffs_height[1], color='red', label=f"Аппроксимация: {coeffs_height[0]:.2f}log(x) + {coeffs_height[1]:.2f}")
plt.xlabel("Количество элементов")
plt.ylabel("Высота")
plt.title("Зависимость высоты")

plt.tight_layout()
plt.show()
