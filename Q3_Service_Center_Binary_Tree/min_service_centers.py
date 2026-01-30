"""
Question 3 - Minimum Service Centers in a Binary Tree
Goal: place the fewest service centers so every node is covered by
itself, its parent, or its children.
"""

"""
APPROACH EXPLANATION:
I used tree dynamic programming with a post-order DFS traversal and state machine.
The approach uses three states:
- State 0: Node needs a service center
- State 1: Node has a service center
- State 2: Node is covered (by parent or children)

Algorithm:
1. Traverse the tree post-order (children before parent)
2. For each node, check children states:
   - If any child needs service (state 0), place a center at current node (state 1)
   - Else if any child has a center (state 1), current node is covered (state 2)
   - Else current node needs service (state 0)
3. After traversing, if root needs service, add one more center
4. Return total centers placed

Time Complexity: O(n) - single tree traversal
Space Complexity: O(h) - recursion stack height (h = tree height)
"""

class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def min_service_centers(root):
    service_centers = 0
    
    """States:
    0 -> needs service
    1 -> has service center
    2 -> covered"""
    
    def dfs(node):
        # Post-order traversal to decide placement from bottom to top.
        nonlocal service_centers
        
        if not node:
            return 2  # Null nodes are considered covered
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # If any child needs service, place a center here.
        if left == 0 or right == 0:
            service_centers += 1
            return 1
        
        # If any child has a center, this node is covered.
        if left == 1 or right == 1:
            return 2
        
        # Otherwise, this node still needs service.
        return 0
    
    root_state = dfs(root)
    
    # Ensure the root is covered.
    if root_state == 0:
        service_centers += 1
        
    return service_centers



class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def min_service_centers(root):
    service_centers = 0
    
    """States:
    0 -> needs service
    1 -> has service center
    2 -> covered"""
    
    def dfs(node):
        # Post-order traversal to decide placement from bottom to top.
        nonlocal service_centers
        
        if not node:
            return 2  # Null nodes are considered covered
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # If any child needs service, place a center here.
        if left == 0 or right == 0:
            service_centers += 1
            return 1
        
        # If any child has a center, this node is covered.
        if left == 1 or right == 1:
            return 2
        
        # Otherwise, this node still needs service.
        return 0
    
    root_state = dfs(root)
    
    # Ensure the root is covered.
    if root_state == 0:
        service_centers += 1
        
    return service_centers

# Example Input Case 1: Balanced tree with 5 nodes
print("=" * 70)
print("INPUT CASE 1: Balanced binary tree with 5 nodes")
print("=" * 70)
print("""
Tree structure:
       0
      / \\
     0   0
    / \\
   0   0
""")

root_1 = TreeNode(0)
root_1.left = TreeNode(0)
root_1.left.right = TreeNode(0)
root_1.left.left = TreeNode(0)
root_1.right = TreeNode(0)

result_1 = min_service_centers(root_1)
print(f"Minimum service centers needed: {result_1}")

# Example Input Case 2: Skewed tree (chain-like)
print("\n" + "=" * 70)
print("INPUT CASE 2: Skewed tree (right chain with 5 nodes)")
print("=" * 70)
print("""
Tree structure:
       0
       |
       0
        \\
         0
          \\
           0
            \\
             0
""")

root_2 = TreeNode(0)
root_2.right = TreeNode(0)
root_2.right.right = TreeNode(0)
root_2.right.right.right = TreeNode(0)
root_2.right.right.right.right = TreeNode(0)

result_2 = min_service_centers(root_2)
print(f"Minimum service centers needed: {result_2}")

"""
OUTPUT CASE 1 (Balanced 5-node tree):
Minimum service centers needed: 2

OUTPUT CASE 2 (Skewed 5-node chain):
Minimum service centers needed: 2
"""

"""
REMARKS:
- The optimal placement depends on tree structure, not just node count.
- For balanced trees, centers are placed strategically to cover multiple nodes.
- For skewed (chain-like) trees, centers must be placed more frequently.
- The state machine ensures every node is either:
  (a) Hosting a center
  (b) A child/parent of a node with a center
  (c) Both children's subtrees are covered
- The DFS approach is greedy: it places centers at the lowest necessary points.
- Edge cases like single-node trees (result = 1) or null trees (result = 0) are
  handled correctly by the post-order logic.
- Different tree shapes can result in the same minimum count (as shown in the
  two cases above, both requiring 2 centers despite different structures).
"""