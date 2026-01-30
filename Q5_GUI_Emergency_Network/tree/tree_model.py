"""
Question 5 - Binary Search Tree: Command Hierarchy Data Structure

Problem Overview:
This module implements a Binary Search Tree (BST) for organizing the command hierarchy
in the emergency response system. Each node represents a command center with a priority
value, and the BST property ensures efficient lookup, insertion, and deletion operations.

Approach:
I implemented a standard BST where for each node:
- All values in left subtree < node value
- All values in right subtree > node value

The tree supports:
1. Insertion: Add new command centers maintaining BST property
2. Deletion: Remove command centers with three cases (leaf, one child, two children)
3. Search: Find command centers by priority value
4. Traversal: In-order, pre-order, post-order for reporting

The BST serves as the foundation for AVL tree rebalancing, which ensures O(log n)
height for all operations instead of potentially O(n) for skewed trees.

Time Complexity (unbalanced):
- Insert: O(h) where h is height (worst O(n), average O(log n))
- Delete: O(h)
- Search: O(h)
- Traversal: O(n)
"""


class TreeNode:
    """Represents a single node in the command hierarchy tree."""
    
    def __init__(self, value, height=1):
        """
        Initialize a tree node.
        
        Parameters:
            value: Data stored in node (command priority or identifier)
            height: Height of node (used for AVL balancing)
        """
        self.value = value
        self.left = None
        self.right = None
        self.height = height
        self.level = 0  # For visualization purposes
    
    def is_leaf(self):
        """Check if node is a leaf (no children)."""
        return self.left is None and self.right is None


class BinarySearchTree:
    """
    Basic Binary Search Tree implementation for command hierarchy.
    Maintains BST property: left < node < right
    
    Time Complexity (without balancing):
        - Insert: O(h) where h = height (worst O(n), average O(log n))
        - Delete: O(h)
        - Search: O(h)
        - Traversal: O(n)
    """
    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, value):
        """
        Insert a value into the tree maintaining BST property.
        Duplicates are not inserted.
        
        Parameters:
            value: Value to insert
        
        Returns:
            success: Whether insertion was successful
        """
        if self.root is None:
            self.root = TreeNode(value)
            self.size = 1
            return True
        
        self.root = self._insert_recursive(self.root, value)
        self.size += 1
        return True
    
    def _insert_recursive(self, node, value):
        """Recursive helper for insertion following BST property."""
        if node is None:
            return TreeNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node  # Duplicate, no insertion
        
        return node
    
    def delete(self, value):
        """
        Delete a value from the tree.
        Handles three cases: leaf, one child, two children.
        
        Parameters:
            value: Value to delete
        
        Returns:
            success: Whether deletion was successful
        """
        if self.root is None:
            return False
        
        old_size = self.size
        self.root = self._delete_recursive(self.root, value)
        
        if self.size < old_size:
            return True
        return False
    
    def _delete_recursive(self, node, value):
        """
        Recursive helper for deletion.
        Uses in-order successor for two-child case.
        """
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Found node to delete
            self.size -= 1
            
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Find inorder successor (smallest in right subtree)
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
        
        return node
    
    def search(self, value):
        """
        Search for a value in the tree.
        
        Time Complexity: O(log n) average, O(n) worst case
        
        Parameters:
            value: Value to search for
        
        Returns:
            found: Whether value exists in tree
        """
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        """Recursive helper for search."""
        if node is None:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def inorder_traversal(self):
        """
        In-order traversal (Left, Root, Right).
        Returns nodes in sorted order.
        
        Time Complexity: O(n)
        
        Returns:
            values: Sorted list of values
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Recursive helper for in-order traversal."""
        if node is None:
            return
        
        self._inorder_recursive(node.left, result)
        result.append(node.value)
        self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self):
        """
        Pre-order traversal (Root, Left, Right).
        Useful for tree reconstruction.
        
        Time Complexity: O(n)
        
        Returns:
            values: Pre-order list of values
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        """Recursive helper for pre-order traversal."""
        if node is None:
            return
        
        result.append(node.value)
        self._preorder_recursive(node.left, result)
        self._preorder_recursive(node.right, result)
    
    def get_height(self):
        """
        Get the height of the tree.
        
        Time Complexity: O(n)
        
        Returns:
            height: Height of tree (0 for empty, 1 for single node)
        """
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node):
        """Recursive helper to calculate height."""
        if node is None:
            return 0
        
        left_height = self._get_height_recursive(node.left)
        right_height = self._get_height_recursive(node.right)
        
        return 1 + max(left_height, right_height)
    
    def is_balanced(self):
        """
        Check if tree is balanced (AVL property).
        
        A tree is balanced if for every node, the difference between
        left and right subtree heights is at most 1.
        
        Time Complexity: O(n)
        
        Returns:
            balanced: Whether tree is balanced
        """
        def check_balance(node):
            if node is None:
                return True, 0
            
            left_balanced, left_height = check_balance(node.left)
            if not left_balanced:
                return False, 0
            
            right_balanced, right_height = check_balance(node.right)
            if not right_balanced:
                return False, 0
            
            is_balanced = abs(left_height - right_height) <= 1
            height = 1 + max(left_height, right_height)
            
            return is_balanced, height
        
        balanced, _ = check_balance(self.root)
        return balanced
    
    def get_max_depth_path_length(self):
        """
        Get length of longest path from root to leaf.
        Used to measure communication path length.
        
        Time Complexity: O(n)
        
        Returns:
            max_depth: Maximum depth
        """
        return self._max_depth_recursive(self.root)
    
    def _max_depth_recursive(self, node):
        """Recursive helper for max depth."""
        if node is None:
            return 0
        
        left_depth = self._max_depth_recursive(node.left)
        right_depth = self._max_depth_recursive(node.right)
        
        return 1 + max(left_depth, right_depth)
    
    def get_all_nodes(self):
        """
        Get all nodes in tree with level information for visualization.
        
        Time Complexity: O(n)
        
        Returns:
            nodes: List of (value, level, node) tuples
        """
        result = []
        self._collect_nodes(self.root, 0, result)
        return result
    
    def _collect_nodes(self, node, level, result):
        """Recursive helper to collect nodes with levels."""
        if node is None:
            return
        
        result.append((node.value, level, node))
        self._collect_nodes(node.left, level + 1, result)
        self._collect_nodes(node.right, level + 1, result)


"""
Remarks:
- BST provides efficient average-case O(log n) operations for balanced trees.
- Worst case O(n) occurs when tree becomes skewed (e.g., inserting sorted data).
- Delete operation handles three cases: leaf (easy), one child (bypass), two children (successor replacement).
- In-order traversal of BST produces sorted sequence - useful for reporting.
- Height tracking enables balance factor calculation for AVL tree extension.
- This base implementation is extended by AVL tree to guarantee O(log n) operations.
"""
