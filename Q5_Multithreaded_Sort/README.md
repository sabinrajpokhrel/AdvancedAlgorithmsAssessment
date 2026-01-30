# Multithreaded Sorting Application

## Overview
This program implements a multithreaded sorting algorithm that divides a list into two halves, sorts each half using separate threads, and then merges them using a third thread.

## Algorithm Description

### Architecture
The program follows a three-phase approach:

1. **Phase 1: Parallel Sorting**
   - The input list is divided into two equal-sized sublists
   - Two sorting threads are created, each responsible for sorting one sublist
   - Both threads run in parallel, sorting their respective portions using merge sort
   - Thread 0 sorts the left half (indices 0 to mid-1)
   - Thread 1 sorts the right half (indices mid to end)

2. **Phase 2: Merging**
   - After both sorting threads complete, a merging thread is created
   - The merging thread combines the two sorted sublists into a single sorted list
   - Uses a standard two-pointer merge algorithm

3. **Phase 3: Output**
   - The parent thread outputs the final sorted array

### Visual Representation
```
Original List: [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
                          |
                   Split into two
                    /           \
    Thread 0              Thread 1
[7, 12, 19, 3, 18]    [4, 2, 6, 15, 8]
       |                     |
    Sort ↓                Sort ↓
[3, 7, 12, 18, 19]    [2, 4, 6, 8, 15]
                    \           /
                   Merge Thread
                         |
                         ↓
        [2, 3, 4, 6, 7, 8, 12, 15, 18, 19]
```

## Implementation Details

### Global Data Structures
- **original_array**: Shared global array that contains the input and is modified by sorting threads
- **sorted_array**: Second global array that stores the final merged result
- **lock**: Threading lock to ensure thread-safe access to shared data

### Functions

#### `merge_sort_algorithm(arr)`
- Standard merge sort implementation
- Time Complexity: O(n log n)
- Space Complexity: O(n)
- Used by each sorting thread to sort its sublist

#### `merge(left, right)`
- Merges two sorted lists into one sorted list
- Time Complexity: O(n + m) where n and m are the lengths of the lists
- Space Complexity: O(n + m)

#### `sorting_thread(thread_id, start_index, end_index)`
- Thread function for sorting a sublist
- Parameters:
  - `thread_id`: Identifier for the thread (0 or 1)
  - `start_index`: Starting index in the global array
  - `end_index`: Ending index in the global array (exclusive)
- Extracts the sublist, sorts it, and writes back to the original array

#### `merging_thread()`
- Thread function for merging two sorted sublists
- Reads the two sorted halves from the original array
- Merges them and stores the result in the sorted_array

#### `multithreaded_sort(input_list)`
- Main function that orchestrates the entire sorting process
- Creates and manages the threads
- Returns the final sorted list

## Time Complexity Analysis

### Sequential Complexity
- Sorting each half: O(n/2 log(n/2)) = O(n log n)
- Merging: O(n)
- Total: O(n log n)

### Parallel Complexity
With 2 sorting threads running in parallel:
- Parallel sorting phase: O(n/2 log(n/2)) = O(n log n) on each thread
- Merging phase: O(n)
- **Total parallel time: O(n/2 log(n/2)) + O(n) = O(n log n)**

### Speedup
- Theoretical speedup: ~2x for the sorting phase (with 2 cores)
- Actual speedup depends on:
  - Number of available CPU cores
  - Thread overhead
  - Lock contention
  - Cache performance

## Space Complexity
- Original array: O(n)
- Sorted array: O(n)
- Merge sort recursion stack: O(log n) per thread
- **Total: O(n)**

## Usage

### Running the Main Program
```bash
python multithreaded_sort.py
```

The program will:
1. Run 4 demonstration test cases
2. Show detailed output for each phase
3. Verify correctness of the results
4. Prompt for custom input (optional)

### Running Tests
```bash
python test_multithreaded_sort.py
```

This runs a comprehensive test suite including:
- Basic case from the diagram
- Already sorted lists
- Reverse sorted lists
- Lists with duplicates
- Edge cases (single element, two elements)
- Large random lists
- Lists with negative numbers

### Using as a Module
```python
from multithreaded_sort import multithreaded_sort

# Sort a list
my_list = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
sorted_list = multithreaded_sort(my_list)
print(sorted_list)  # [2, 3, 4, 6, 7, 8, 12, 15, 18, 19]
```

## Features

### Thread Safety
- Uses threading locks to ensure thread-safe access to shared data
- Prevents race conditions when multiple threads access global arrays

### Detailed Logging
- Shows the progress of each thread
- Displays sublists before and after sorting
- Shows the merging process
- Verifies correctness of results

### Comprehensive Testing
- Multiple test cases covering various scenarios
- Verification against Python's built-in sort
- Edge case handling

## Advantages of This Approach

1. **Parallelism**: Takes advantage of multiple CPU cores
2. **Scalability**: Can be extended to more threads for larger datasets
3. **Modularity**: Clear separation of sorting and merging logic
4. **Thread Safety**: Proper synchronization using locks
5. **Verification**: Built-in correctness checking

## Limitations

1. **Two Threads Only**: Currently uses only 2 sorting threads
2. **Global State**: Relies on global variables (could be refactored to use classes)
3. **Fixed Division**: Always divides the list into two equal halves
4. **Overhead**: Thread creation and synchronization overhead for small lists

## Possible Enhancements

1. **Variable Thread Count**: Allow sorting with more than 2 threads
2. **Dynamic Load Balancing**: Distribute work based on sublist sizes
3. **Thread Pool**: Reuse threads to reduce creation overhead
4. **Adaptive Algorithm**: Use different sorting algorithms for small sublists
5. **Class-Based Design**: Encapsulate state in a class instead of globals

## Testing Results

All test cases pass successfully:
- ✓ Basic case from diagram
- ✓ Already sorted list
- ✓ Reverse sorted list
- ✓ List with duplicates
- ✓ Single element
- ✓ Two elements
- ✓ Large random list (100 elements)
- ✓ List with negative numbers

## Conclusion

This implementation successfully demonstrates a multithreaded sorting approach where:
- Work is divided among multiple threads
- Each thread independently sorts its portion
- A separate thread merges the results
- Thread synchronization ensures correctness
- The final result is a properly sorted list

The program follows the exact specification from the assignment and produces correct results for all test cases.
