def max_points(tile_multipliers):
    tiles = [1] + tile_multipliers + [1]
    n = len(tiles)
    
    dp = [[0]* n for _ in range(n)]
    
    for length in range(2, n):
        for i in range(0, n - length):
            j = i + length
            
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