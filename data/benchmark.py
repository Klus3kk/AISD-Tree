import time
import numpy as np
import os
from bst import binTreeNode, makeAvlTree

def read_data(file_path):
    return np.loadtxt(file_path, dtype=int)

def create_bst(data):
    tree = binTreeNode(tree_type='bst')
    for num in data:
        tree.insert(num)
    return tree

def create_avl(data):
    return makeAvlTree(sorted(data))

def find_min_max(tree):
    return tree.findMin(), tree.findMax()

def print_in_order(tree):
    output = []
    stack = []
    current = tree

    while stack or current:
        if current:
            stack.append(current)
            current = current.left
        else:
            current = stack.pop()
            output.append(current.key)
            current = current.right

    return output


def rebalance_bst(tree):
    return tree.convert_to_avl()

def measure_time(function, *args, runs=2):
    """Measure the average execution time of a function over a specified number of runs."""
    total_time = 0
    for _ in range(runs):
        start = time.perf_counter()
        function(*args)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / runs

def benchmark(directory):
    data_types = ['random', 'increasing', 'decreasing', 'a_shaped', 'constant']
    sizes = range(10000, 100001, 10000)

    for data_type in data_types:
        results = []
        for size in sizes:
            file_path = f'{directory}/{data_type}_{size:08d}.txt'
            if not os.path.exists(file_path):
                continue
            print(f"Processing {file_path}...")
            data = read_data(file_path)
            data = data[1:]  # Exclude the first element if it's not part of the tree

            # Create both trees
            bst = create_bst(data)
            avl = create_avl(data)

            # Measure time for all required operations
            time_bst_creation = measure_time(create_bst, data)
            time_avl_creation = measure_time(create_avl, data)
            time_bst_find_min_max = measure_time(find_min_max, bst)
            time_avl_find_min_max = measure_time(find_min_max, avl)
            time_bst_in_order = measure_time(print_in_order, bst) if data_type == 'random' else float('nan')  # Skip skewed BSTs
            time_avl_in_order = measure_time(print_in_order, avl)
            time_rebalance = measure_time(rebalance_bst, bst)

            results.append([
                size,
                time_bst_creation, time_avl_creation,
                time_bst_find_min_max, time_avl_find_min_max,
                time_bst_in_order, time_avl_in_order,
                time_rebalance
            ])

        header = "Size,BST Creation,AVL Creation,BST Find Min/Max,AVL Find Min/Max,BST In-Order,AVL In-Order,Rebalance BST"
        np.savetxt(f"benchmark_results_{data_type}.csv", results, delimiter=",", fmt="%0.7f", header=header, comments="")

if __name__ == "__main__":
    benchmark_directory = './benchmark'
    benchmark(benchmark_directory)
