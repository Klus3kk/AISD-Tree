import sys

from bst import *  
from tikz import *  

def read_initial_tree():
    num_nodes = int(input('nodes> '))
    nodes_input = input('insert> ')
    numbers = list(map(int, nodes_input.strip().split()))
    return numbers

def display_help():
    print("\nAvailable commands:")
    print("Help       - Show this message")
    print("FindMinMax - Print the smallest and the largest node from the tree")
    print("Print      - Print the tree using In-order, Pre-order, Post-order")        
    print("Remove     - Remove an element from the tree")
    print("Delete     - Delete the whole tree")
    print("Export     - Export the tree to TikZ picture")
    print("Rebalance  - Rebalance the AVL tree or convert BST to AVL and rebalance")
    print("Exit       - Exit the program (same as ctrl+C)")

def process_command(command, tree, tree_type):
    args = command.split()
    cmd = args[0].lower()

    if cmd == 'help':
        display_help()
    elif cmd == 'print':
        if not tree.key:
            print(f"{tree_type.upper()} tree is empty.")
        else:
            print(" Pre-order: ", end="")
            tree.traverse_pre_order()
            print("\n  In-order: ", end="")
            tree.traverse_in_order()
            print("\nPost-order: ", end="")
            tree.traverse_post_order()
            print()
    elif cmd == 'remove':
        print('nodes> ', end='')
        num_nodes_to_delete = int(input())
        print('delete> ', end='')
        nodes_to_delete = list(map(int, input().strip().split()))
            
        if len(nodes_to_delete) != num_nodes_to_delete:
            print(f"Error: Expected {num_nodes_to_delete} nodes, got {len(nodes_to_delete)}")
        else:
            for value in nodes_to_delete:
                if tree.delete(value):
                    print(f"Removed {value}")
                else:
                    print(f"Value {value} not found")
                    
                if tree_type == 'avl':  
                    tree.rebalance()
    elif cmd == 'delete':
        tree.delete_tree()
        print("Tree succesfully deleted.")
    elif cmd == 'export':
        filename = input('Enter the filename to save the tree structure: ') + ".tex"
        export(tree, filename)
        print('Tree exported successfully.')
    elif cmd == 'rebalance':
        if tree_type == 'bst':
            tree = tree.convert_to_avl()  # Convert BST to AVL
            tree_type = 'avl'  # Update tree type to AVL
            print("Converted BST to AVL and rebalanced.")
        if tree_type == 'avl':
            tree.rebalance()
        print("Tree rebalanced. \nPre-Order: ", end="")
        tree.traverse_pre_order()
        print()
    elif cmd == 'findminmax':
        min_value = tree.findMin()
        max_value = tree.findMax()
        print(f"Min: {min_value}\nMax: {max_value}")
    elif cmd == 'exit':
        print('Exiting...')
        sys.exit(0)
    else:
        print('Invalid command. Type "help" for a list of commands.')

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--tree':
        print("Please specify the tree type with 'python3 main.py --tree AVL' or 'python3 main.py --tree BST'.")
        sys.exit(1)

    tree_type = sys.argv[2].lower()

    numbers = read_initial_tree()

    if tree_type == 'avl':
        tree = makeAvlTree(numbers)  
    else:
        tree = binTreeNode(tree_type='bst')  
        for num in numbers:
            tree.insert(num)

    while True:
        try:
            command = input('\naction> ')
            process_command(command, tree, tree_type)  
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()


