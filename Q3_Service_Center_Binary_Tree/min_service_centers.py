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
        nonlocal service_centers
        
        if not node:
            return 2  # Null nodes are considered covered
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        if left == 0 or right == 0:
            service_centers += 1
            return 1
        
        if left ==1 or right ==1:
            return 2
        
        return 0
    
    root_state = dfs(root)
    
    if root_state == 0:
        service_centers += 1
        
    return service_centers

# Example usage:
root = TreeNode(0)
root.left = TreeNode(0)
root.left.right = TreeNode(0)
root.left.right.left = TreeNode(0)
root.left.right.left.right = TreeNode(0)

result = min_service_centers(root)
print("The minimum number of service centers needed is:", result)