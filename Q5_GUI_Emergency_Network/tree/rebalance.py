"""
Question 5 - AVL Tree Rebalancing: Self-Balancing Binary Search Tree

Problem Overview:
In a command hierarchy system, we need fast access to command centers by priority.
A regular BST can become skewed with O(n) height, making operations slow. AVL tree
solves this by automatically rebalancing after every insert/delete to maintain
O(log n) height guarantee.

Approach:
I implemented AVL tree by extending the basic BST with automatic rebalancing using rotations.
The AVL property states: for every node, |height(left) - height(right)| ≤ 1

After each insertion or deletion, I:
1. Update height of affected nodes
2. Calculate balance factor = height(left) - height(right)
3. If |balance_factor| > 1, apply rotations to restore balance

Four rotation cases:
- Left-Left: Right rotation
- Right-Right: Left rotation
- Left-Right: Left rotation on left child, then right rotation
- Right-Left: Right rotation on right child, then left rotation

Rotations preserve BST property while reducing height, ensuring O(log n) for all operations.

Time Complexity (guaranteed):
- Insert: O(log n)
- Delete: O(log n)
- Search: O(log n)
- Rotations: O(1) per rotation
"""

from tree.tree_model import TreeNode, BinarySearchTree


class AVLTree(BinarySearchTree):
    """
    Self-balancing binary search tree using AVL rotations.
    Maintains balance through rotations after insert/delete.
    
    Time Complexity (all operations guaranteed):
        - Insert: O(log n)
        - Delete: O(log n)
        - Search: O(log n)
    Space Complexity: O(n) + O(log n) for recursion stack
    """
    
    def insert(self, value):
        """
        Insert with automatic rebalancing.
        
        Parameters:
            value: Value to insert
        """
        if self.root is None:
            self.root = TreeNode(value, 1)
            self.size = 1
            return True
        
        old_size = self.size
        self.root = self._insert_avl_recursive(self.root, value)
        
        if self.size > old_size:
            return True
        return False
    
    def _insert_avl_recursive(self, node, value):
        """Insert with AVL rebalancing."""
        if node is None:
            self.size += 1
            return TreeNode(value, 1)
        
        if value < node.value:
            node.left = self._insert_avl_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_avl_recursive(node.right, value)
        else:
            return node  # Duplicate
        
        # Update height
        node.height = 1 + max(self._get_height(node.left), 
                              self._get_height(node.right))
        
        # Check balance factor and rebalance if needed
        return self._rebalance(node)
    
    def delete(self, value):
        """
        Delete with automatic rebalancing.
        
        Parameters:
            value: Value to delete
        """
        if self.root is None:
            return False
        
        old_size = self.size
        self.root = self._delete_avl_recursive(self.root, value)
        
        return self.size < old_size
    
    def _delete_avl_recursive(self, node, value):
        """Delete with AVL rebalancing."""
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_avl_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_avl_recursive(node.right, value)
        else:
            # Node to delete found
            self.size -= 1
            
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Find inorder successor
                successor_parent = node
                successor = node.right
                
                while successor.left is not None:
                    successor_parent = successor
                    successor = successor.left
                
                node.value = successor.value
                
                if successor_parent == node:
                    node.right = successor.right
                else:
                    successor_parent.left = successor.right
        
        if node is None:
            return None
        
        # Update height and rebalance
        node.height = 1 + max(self._get_height(node.left),
                              self._get_height(node.right))
        
        return self._rebalance(node)
    
    def _get_height(self, node):
        """Get height of a node."""
        return node.height if node is not None else 0
    
    def _get_balance_factor(self, node):
        """
        Calculate balance factor (height difference).
        
        Returns:
            balance: left_height - right_height
        """
        if node is None:
            return 0
        
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rebalance(self, node):
        """
        Rebalance node using rotations.
        
        Handles 4 cases:
        1. Left-Left: Right rotation
        2. Left-Right: Left rotation, then right rotation
        3. Right-Right: Left rotation
        4. Right-Left: Right rotation, then left rotation
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        balance = self._get_balance_factor(node)
        
        # Left heavy
        if balance > 1:
            if self._get_balance_factor(node.left) < 0:
                # Left-Right case
                node.left = self._rotate_left(node.left)
            
            # Left-Left case
            return self._rotate_right(node)
        
        # Right heavy
        if balance < -1:
            if self._get_balance_factor(node.right) > 0:
                # Right-Left case
                node.right = self._rotate_right(node.right)
            
            # Right-Right case
            return self._rotate_left(node)
        
        return node
    
    def _rotate_right(self, y):
        """
        Right rotation:
          y                    x
         / \                  / \
        x   C      =>        A   y
       / \                      / \
      A   B                    B   C
        
        Time Complexity: O(1)
        """
        x = y.left
        B = x.right
        
        # Perform rotation
        x.right = y
        y.left = B
        
        # Update heights
        y.height = 1 + max(self._get_height(y.left),
                          self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left),
                          self._get_height(x.right))
        
        return x
    
    def _rotate_left(self, x):
        """
        Left rotation:
          x                      y
         / \                    / \
        A   y        =>        x   C
           / \                / \
          B   C              A   B
        
        Time Complexity: O(1)
        """
        y = x.right
        B = y.left
        
        # Perform rotation
        y.left = x
        x.right = B
        
        # Update heights
        x.height = 1 + max(self._get_height(x.left),
                          self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left),
                          self._get_height(y.right))
        
        return y
    
    def get_max_depth_path_length(self):
        """
        Get maximum depth in AVL tree.
        After balancing, this is O(log n).
        
        Time Complexity: O(n) but bounded by O(log n) in balanced tree
        
        Returns:
            max_depth: Maximum path length from root to leaf
        """
        return self._max_depth_recursive(self.root)
    
    def _max_depth_recursive(self, node):
        """Recursive helper for max depth."""
        if node is None:
            return 0
        
        left_depth = self._max_depth_recursive(node.left)
        right_depth = self._max_depth_recursive(node.right)
        
        return 1 + max(left_depth, right_depth)


def rebalance_tree(old_tree):
    """
    Rebalance an existing BST to AVL tree.
    
    Algorithm:
    1. Extract all values in sorted order (inorder traversal)
    2. Build balanced BST by inserting median elements first (recursive)
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Parameters:
        old_tree (BinarySearchTree): Tree to rebalance
    
    Returns:
        avl_tree (AVLTree): Balanced AVL tree with same values
    """
    
    # Get all values in sorted order
    values = old_tree.inorder_traversal()
    
    if not values:
        avl_tree = AVLTree()
        return avl_tree
    
    # Build AVL tree by inserting in order that creates balance
    avl_tree = AVLTree()
    _build_balanced_tree(avl_tree, values, 0, len(values) - 1)
    
    return avl_tree


def _build_balanced_tree(avl_tree, sorted_values, low, high):
    """
    Recursive helper to build balanced tree from sorted array.
    
    Algorithm:
    1. Find middle element
    2. Insert it to create root
    3. Recursively build left subtree (elements below middle)
    4. Recursively build right subtree (elements above middle)
    
    Time Complexity: O(n)
    
    Parameters:
        avl_tree: AVL tree to insert into
        sorted_values: Array of sorted values
        low: Low index
        high: High index
    """
    
    if low <= high:
        mid = (low + high) // 2
        avl_tree.insert(sorted_values[mid])
        
        _build_balanced_tree(avl_tree, sorted_values, low, mid - 1)
        _build_balanced_tree(avl_tree, sorted_values, mid + 1, high)


def analyze_tree_balance(tree):
    """
    Analyzes balance characteristics of a tree.
    
    Parameters:
        tree (BinarySearchTree): Tree to analyze
    
    Returns:
        analysis: Dictionary with balance metrics
    """
    
    analysis = {
        'is_balanced': tree.is_balanced(),
        'height': tree.get_height(),
        'size': tree.size,
        'max_path_length': tree.get_max_depth_path_length(),
        'balance_factor': 'Balanced' if tree.is_balanced() else 'Unbalanced',
        'optimal_height': _calculate_optimal_height(tree.size),
        'height_overhead': tree.get_height() - _calculate_optimal_height(tree.size)
    }
    
    return analysis


def _calculate_optimal_height(n):
    """Calculate optimal height for n nodes (log2(n+1))."""
    if n <= 0:
        return 0
    
    height = 0
    power = 1
    while power <= n:
        height += 1
        power *= 2
    
    return height


"""
Remarks:
- AVL tree guarantees O(log n) height, eliminating worst-case O(n) of unbalanced BST.
- Four rotation types handle all imbalance scenarios after insert/delete operations.
- Path compression during rotations maintains O(1) rotation cost.
- Balance factor calculation (left_height - right_height) determines rotation type needed.
- Rebalancing algorithm converts any BST to AVL by sorting values and building balanced tree.
- Height tracking at each node enables efficient balance factor computation.
- AVL trees maintain stricter balance than Red-Black trees (better search, more rotations).
"""
