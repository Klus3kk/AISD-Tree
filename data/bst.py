class binTreeNode:
    def __init__(self, key=None, parent=None, left=None, right=None, tree_type='bst'):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 1  
        self.tree_type = tree_type  

    def insert(self, value):
        if not self.key:
            self.key = value
            return

        current = self
        while True:
            if value < current.key:
                if current.left is None:
                    current.left = binTreeNode(key=value, parent=current)
                    break
                else:
                    current = current.left
            else:  # Assuming no duplicates
                if current.right is None:
                    current.right = binTreeNode(key=value, parent=current)
                    break
                else:
                    current = current.right

        if self.tree_type == 'avl':
            self.rebalance()  # This assumes rebalance can be called here; depends on implementation details

    def findMin(self):
        current = self
        while current.left is not None:
            current = current.left
        return current.key

    def findMax(self):
        current = self
        while current.right is not None:
            current = current.right
        return current.key
    
    def search(self, value):
        if value < self.key and self.left:
            return self.left.search(value)
        elif value > self.key and self.right:
            return self.right.search(value)
        return self if self.key == value else None
    
    def delete(self, value):
        node = self.search(value)
        if not node:
            return False

        parent = node.parent
        if node.left and node.right:
            successor = node.right
            while successor.left:
                successor = successor.left
            node.key = successor.key
            return successor.delete(successor.key)
        elif node.left or node.right:
            child = node.left if node.left else node.right
            if parent:
                if parent.left == node:
                    parent.left = child
                else:
                    parent.right = child
            child.parent = parent
        else:
            if parent:
                if parent.left == node:
                    parent.left = None
                else:
                    parent.right = None

        if self.tree_type == 'avl' and parent:
            self.rebalance_from_node(parent)

        return True



    def traverse_pre_order(self):
        print(self.key, end=' ')
        if self.left:
            self.left.traverse_pre_order()
        if self.right:
            self.right.traverse_pre_order()

    def traverse_in_order(self):
        if self.left:
            self.left.traverse_in_order()
        print(self.key, end=' ')
        if self.right:
            self.right.traverse_in_order()

    def traverse_post_order(self):
        if self.left:
            self.left.traverse_post_order()
        if self.right:
            self.right.traverse_post_order()
        print(self.key, end=' ')
            
    def delete_tree(self):
        if self.left:
            self.left.delete_tree()
            self.left = None
        if self.right:
            self.right.delete_tree()
            self.right = None
        self.key = None
    
    def convert_to_avl(self):
        in_order_keys = []
        stack = []
        current = self

        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                in_order_keys.append(current.key)
                current = current.right

        return makeAvlTree(in_order_keys)


    
    # AVL
    def update_height(self):
        self.height = 1 + max(self.left.height if self.left else 0, self.right.height if self.right else 0)

    def get_balance(self):
        return (self.left.height if self.left else 0) - (self.right.height if self.right else 0)

    def rotate_left(self):
        y = self.right
        self.right = y.left
        if y.left:
            y.left.parent = self
        y.parent = self.parent
        
        if y.parent:
            if y.parent.left == self:
                y.parent.left = y
            else:
                y.parent.right = y

        self.parent = y
        self.update_height()
        y.update_height()
        
        return y

    def rotate_right(self):
        x = self.left
        self.left = x.right
        if x.right:
            x.right.parent = self
        x.parent = self.parent
        
        if x.parent:
            if x.parent.left == self:
                x.parent.left = x
            else:
                x.parent.right = x

        self.parent = x
        self.update_height()
        x.update_height()
        
        return x

    def size(self):
        if self.key is None:
            return 0
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return 1 + left_size + right_size

    def rebalance(self):
        self.update_height()
        balance = self.get_balance()
        if balance > 1:
            if self.left and self.left.get_balance() >= 0:
                return self.rotate_right()
            elif self.left and self.left.get_balance() < 0:
                self.left = self.left.rotate_left()
                return self.rotate_right()

        elif balance < -1:
            if self.right and self.right.get_balance() <= 0:
                return self.rotate_left()
            elif self.right and self.right.get_balance() > 0:
                self.right = self.right.rotate_right()
                return self.rotate_left()

        return self

    
    def rebalance_from_node(self, node):
        while node:
            node.update_height()
            balance = node.get_balance()
            
            if balance > 1:
                if node.left and node.left.get_balance() >= 0:
                    node = node.rotate_right()
                elif node.left and node.left.get_balance() < 0:
                    node.left = node.left.rotate_left()
                    node = node.rotate_right()

            elif balance < -1:
                if node.right and node.right.get_balance() <= 0:
                    node = node.rotate_left()
                elif node.right and node.right.get_balance() > 0:
                    node.right = node.right.rotate_right()
                    node = node.rotate_left()

            node = node.parent  # Przejście do rodzica, aby kontynuować rebalansowanie w górę drzewa


def bisection(l, parentNode=None):
    if not l:
        return None

    medianIdx = (len(l) - 1) // 2
    med = l[medianIdx]
    node = binTreeNode(key=med, parent=parentNode, tree_type='avl')

    if len(l) < 2:
        return node

    node.left = bisection(l[:medianIdx], node)
    node.right = bisection(l[medianIdx+1:], node)

    node.update_height()  
    node = node.rebalance()
    return node



def makeAvlTree(l):
    l.sort()
    return bisection(l)
