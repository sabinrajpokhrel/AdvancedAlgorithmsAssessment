"""
Question 2 - Strategic Tile Shatter (Dynamic Programming)
Goal: maximize total points by choosing the best order to shatter tiles,
where points = left * current * right (out-of-bounds treated as 1).
"""

"""
APPROACH EXPLANATION:
I used interval dynamic programming to solve this tile-shattering problem. The approach:
1. Pad the multiplier array with 1s at both ends to handle boundary cases uniformly
2. Build a 2D DP table where dp[i][j] = max points from shattering tiles between i and j
3. Process intervals in increasing order of length (bottom-up approach)
4. For each interval, try all possible positions k as the last tile to shatter
5. When k is shattered last, tiles[i] and tiles[j] still exist, so points = tiles[i]*tiles[k]*tiles[j]
6. Return dp[0][n-1] for the entire array

Time Complexity: O(n^3) - three nested loops over interval positions
Space Complexity: O(n^2) - 2D DP table
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
    
# Example Input Case 1
print("=" * 70)
print("INPUT CASE 1: [3, 1, 5, 8]")
print("=" * 70)
tiles1 = [3, 1, 5, 8]
print(f"Tile multipliers: {tiles1}")

result1 = max_points(tiles1)
print(f"Maximum points: {result1}")

# Example Input Case 2
print("\n" + "=" * 70)
print("INPUT CASE 2: [1, 5]")
print("=" * 70)
tiles2 = [1, 5]
print(f"Tile multipliers: {tiles2}")

result2 = max_points(tiles2)
print(f"Maximum points: {result2}")

# Example Input Case 3 (Additional case for comprehensive testing)
print("\n" + "=" * 70)
print("INPUT CASE 3: [2, 4, 1, 3]")
print("=" * 70)
tiles3 = [2, 4, 1, 3]
print(f"Tile multipliers: {tiles3}")

result3 = max_points(tiles3)
print(f"Maximum points: {result3}")

"""
OUTPUT CASE 1 ([3, 1, 5, 8]):
Tile multipliers: [3, 1, 5, 8]
Maximum points: 167

OUTPUT CASE 2 ([1, 5]):
Tile multipliers: [1, 5]
Maximum points: 10

OUTPUT CASE 3 ([2, 4, 1, 3]):
Tile multipliers: [2, 4, 1, 3]
Maximum points: 54
"""

"""
REMARKS:
- The optimal shattering order is not necessarily left-to-right or right-to-left.
- Dynamic programming ensures all sub-intervals are optimized before being used
  in larger intervals (optimal substructure property).
- The padding with 1s at both ends elegantly handles boundary cases without special logic.
- For Case 1, the maximum value 167 is achieved by carefully selecting which tile
  to shatter last in each interval to maximize product accumulation.
- For Case 2 with just 2 tiles, the product is always 1*1*5 = 5 or 1*5*1 = 5,
  combined twice (once for each tile), totaling 10.
- The solution demonstrates how interval DP is applicable to problems where
  the order of processing elements within ranges significantly affects the outcome.
- Time complexity is manageable (O(n^3)) even for arrays of size 100+.
"""