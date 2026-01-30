"""
Question 2 - Strategic Tile Shatter (Dynamic Programming)
Goal: maximize total points by choosing the best order to shatter tiles,
where points = left * current * right (out-of-bounds treated as 1).
"""

def max_points(tile_multipliers):
    # Pad with 1 at both ends to handle boundary tiles uniformly.
    tiles = [1] + tile_multipliers + [1]
    n = len(tiles)
    
    # dp[i][j] = max points from shattering tiles strictly between i and j.
    dp = [[0]* n for _ in range(n)]
    
    # Build solutions by increasing interval length.
    for length in range(2, n):
        for i in range(0, n - length):
            j = i + length
            
            # Choose k as the last tile to shatter within (i, j).
            for k in range(i+1, j):
                points = (
                    dp[i][k] + dp[k][j] + tiles[i] * tiles[k] * tiles[j]
                )
                dp[i][j] = max(dp[i][j], points)
                
    return dp[0][n-1]
    

# Example usage:
tiles1 = [3, 1, 5, 8]
print(max_points(tiles1))

tiles2 = [1, 5]
print(max_points(tiles2))

"""
Output (example):
167
10
"""

"""
Remarks:
- Dynamic programming ensures all sub-intervals are optimized.
- Output matches the sample sequences in the question statement.
"""