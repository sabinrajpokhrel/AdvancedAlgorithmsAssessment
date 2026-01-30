"""
Multithreaded Sorting Application
----------------------------------
This program divides a list of integers into two halves, sorts each half
using separate threads, and then merges them using a third thread.

Algorithm:
1. Split the original list into two equal-sized sublists
2. Create two sorting threads to sort each sublist
3. Create a merge thread to combine the sorted sublists
4. Output the final sorted list
"""

import threading
import time


# Global arrays
original_array = []
sorted_array = []
lock = threading.Lock()


def merge_sort_algorithm(arr):
    """
    Standard merge sort implementation for individual sublists.
    Time Complexity: O(n log n)
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_algorithm(arr[:mid])
    right = merge_sort_algorithm(arr[mid:])
    
    return merge(left, right)


def merge(left, right):
    """
    Merge two sorted lists into one sorted list.
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def sorting_thread(thread_id, start_index, end_index):
    """
    Sorting thread function that sorts a sublist of the global array.
    
    Args:
        thread_id: Identifier for the thread
        start_index: Starting index in the global array
        end_index: Ending index in the global array (exclusive)
    """
    print(f"Sorting Thread {thread_id} started: sorting elements from index {start_index} to {end_index-1}")
    
    # Extract sublist
    sublist = original_array[start_index:end_index]
    print(f"Sorting Thread {thread_id}: Original sublist = {sublist}")
    
    # Sort the sublist using merge sort
    sorted_sublist = merge_sort_algorithm(sublist)
    
    # Write back to the original array
    with lock:
        for i, val in enumerate(sorted_sublist):
            original_array[start_index + i] = val
    
    print(f"Sorting Thread {thread_id}: Sorted sublist = {sorted_sublist}")
    print(f"Sorting Thread {thread_id} completed")


def merging_thread():
    """
    Merging thread function that merges two sorted sublists into the final sorted array.
    """
    print("\nMerging Thread started: merging two sorted sublists")
    
    # Split the array into two halves
    mid = len(original_array) // 2
    left_half = original_array[:mid]
    right_half = original_array[mid:]
    
    print(f"Merging Thread: Left half = {left_half}")
    print(f"Merging Thread: Right half = {right_half}")
    
    # Merge the two sorted halves
    merged = merge(left_half, right_half)
    
    # Store in global sorted array
    with lock:
        sorted_array.clear()
        sorted_array.extend(merged)
    
    print(f"Merging Thread: Merged result = {merged}")
    print("Merging Thread completed")


def multithreaded_sort(input_list):
    """
    Main function to perform multithreaded sorting.
    
    Args:
        input_list: List of integers to be sorted
        
    Returns:
        Sorted list of integers
    """
    global original_array, sorted_array
    
    # Initialize global arrays
    original_array = input_list.copy()
    sorted_array = []
    
    print("=" * 60)
    print("MULTITHREADED SORTING APPLICATION")
    print("=" * 60)
    print(f"Original list: {original_array}")
    print(f"List size: {len(original_array)}")
    print("=" * 60)
    
    # Calculate midpoint
    mid = len(original_array) // 2
    
    # Create sorting threads
    print("\nPhase 1: Creating sorting threads...")
    thread0 = threading.Thread(target=sorting_thread, args=(0, 0, mid))
    thread1 = threading.Thread(target=sorting_thread, args=(1, mid, len(original_array)))
    
    # Start sorting threads
    thread0.start()
    thread1.start()
    
    # Wait for sorting threads to complete
    thread0.join()
    thread1.join()
    
    print("\n" + "=" * 60)
    print("Phase 1 Complete: Both sorting threads finished")
    print(f"Array after sorting threads: {original_array}")
    print("=" * 60)
    
    # Create and start merging thread
    print("\nPhase 2: Creating merging thread...")
    merge_thread = threading.Thread(target=merging_thread)
    merge_thread.start()
    
    # Wait for merging thread to complete
    merge_thread.join()
    
    print("\n" + "=" * 60)
    print("Phase 2 Complete: Merging thread finished")
    print("=" * 60)
    print(f"\nFinal sorted list: {sorted_array}")
    print("=" * 60)
    
    return sorted_array


def demonstrate():
    """
    Demonstration function with various test cases.
    """
    test_cases = [
        [7, 12, 19, 3, 18, 4, 2, 6, 15, 8],  # From the diagram
        [64, 34, 25, 12, 22, 11, 90, 88],
        [5, 2, 8, 1, 9],
        [100, 50, 25, 75, 10, 90, 40, 60],
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n\n{'#' * 60}")
        print(f"TEST CASE {i + 1}")
        print(f"{'#' * 60}")
        result = multithreaded_sort(test_case)
        
        # Verify correctness
        expected = sorted(test_case)
        if result == expected:
            print(f"\n✓ VERIFICATION: Sorting is CORRECT!")
        else:
            print(f"\n✗ VERIFICATION: Sorting is INCORRECT!")
            print(f"Expected: {expected}")
        
        time.sleep(0.5)  # Small delay between test cases for readability


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MULTITHREADED SORTING APPLICATION")
    print("Divides list into two halves, sorts each with a separate thread,")
    print("and merges them with a third thread.")
    print("=" * 60)
    
    # Run demonstration
    demonstrate()
    
    print("\n\n" + "=" * 60)
    print("CUSTOM INPUT")
    print("=" * 60)
    
    # Allow custom input
    try:
        user_input = input("\nEnter integers separated by spaces (or press Enter to skip): ").strip()
        if user_input:
            custom_list = list(map(int, user_input.split()))
            result = multithreaded_sort(custom_list)
            print(f"\nVerification: {result == sorted(custom_list)}")
        else:
            print("Skipping custom input.")
    except ValueError:
        print("Invalid input. Please enter integers separated by spaces.")
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    
    print("\n" + "=" * 60)
    print("Program completed successfully!")
    print("=" * 60)
