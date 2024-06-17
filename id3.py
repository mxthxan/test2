import numpy as np
import math
import csv

def read_data(filename):
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        headers = next(datareader)
        metadata = headers
        traindata = [row for row in datareader]
    return metadata, traindata

class Node:
    def __init__(self, attribute):
        self.attribute = attribute
        self.children = []
        self.answer = ""

    def __str__(self):
        return self.attribute

def subtables(data, col, delete):
    unique_items = np.unique(data[:, col])
    subtable_dict = {}
    
    for item in unique_items:
        subtable = data[data[:, col] == item]
        if delete:
            subtable = np.delete(subtable, col, axis=1)
        subtable_dict[item] = subtable
    
    return unique_items, subtable_dict

def entropy(S):
    unique_items, counts = np.unique(S, return_counts=True)
    probabilities = counts / len(S)
    
    return -np.sum(probabilities * np.log2(probabilities))

def gain_ratio(data, col):
    items, subtable_dict = subtables(data, col, delete=False)
    total_entropy = entropy(data[:, -1])
    
    weighted_entropy = 0
    intrinsic_value = 0
    total_size = len(data)
    
    for item in items:
        subtable = subtable_dict[item]
        ratio = len(subtable) / total_size
        weighted_entropy += ratio * entropy(subtable[:, -1])
        intrinsic_value -= ratio * np.log2(ratio)
    
    information_gain = total_entropy - weighted_entropy
    if intrinsic_value == 0:  # Prevent division by zero
        return 0
    
    return information_gain / intrinsic_value

def create_node(data, metadata):
    if len(np.unique(data[:, -1])) == 1:
        node = Node("")
        node.answer = np.unique(data[:, -1])[0]
        return node
    
    gains = np.array([gain_ratio(data, col) for col in range(data.shape[1] - 1)])
    best_col = np.argmax(gains)
    
    node = Node(metadata[best_col])
    new_metadata = np.delete(metadata, best_col)
    
    items, subtable_dict = subtables(data, best_col, delete=True)
    
    for item in items:
        child = create_node(subtable_dict[item], new_metadata)
        node.children.append((item, child))
    
    return node

def empty(size):
    return "   " * size

def print_tree(node, level=0):
    if node.answer:
        print(f"{empty(level)}{node.answer}")
    else:
        print(f"{empty(level)}{node.attribute}")
        for value, child in node.children:
            print(f"{empty(level + 1)}{value}")
            print_tree(child, level + 2)

# File name
filename = "tennis.csv"
metadata, traindata = read_data(filename)
data = np.array(traindata, dtype=object)
node = create_node(data, np.array(metadata, dtype=object))
print_tree(node, 0)
