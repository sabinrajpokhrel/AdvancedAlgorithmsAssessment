"""
Test suite for the multithreaded sorting application
"""

from multithreaded_sort import multithreaded_sort
import random


def test_basic_case():
    """Test the example from the diagram"""
    input_list = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
    result = multithreaded_sort(input_list)
    expected = [2, 3, 4, 6, 7, 8, 12, 15, 18, 19]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Test 1 passed: Basic case from diagram")


def test_already_sorted():
    """Test with already sorted list"""
    input_list = [1, 2, 3, 4, 5, 6, 7, 8]
    result = multithreaded_sort(input_list)
    expected = sorted(input_list)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Test 2 passed: Already sorted list")


def test_reverse_sorted():
    """Test with reverse sorted list"""
    input_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    result = multithreaded_sort(input_list)
    expected = sorted(input_list)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Test 3 passed: Reverse sorted list")


def test_duplicates():
    """Test with duplicate values"""
    input_list = [5, 2, 8, 2, 9, 1, 5, 8]
    result = multithreaded_sort(input_list)
    expected = sorted(input_list)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Test 4 passed: List with duplicates")


def test_single_element():
    """Test with single element"""
    input_list = [42]
    result = multithreaded_sort(input_list)
    expected = [42]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Test 5 passed: Single element")


def test_two_elements():
    """Test with two elements"""
    input_list = [5, 2]
    result = multithreaded_sort(input_list)
    expected = [2, 5]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Test 6 passed: Two elements")


def test_large_random():
    """Test with larger random list"""
    input_list = [random.randint(1, 1000) for _ in range(100)]
    result = multithreaded_sort(input_list)
    expected = sorted(input_list)
    assert result == expected, f"Lists don't match"
    print("✓ Test 7 passed: Large random list (100 elements)")


def test_negative_numbers():
    """Test with negative numbers"""
    input_list = [-5, 3, -1, 8, -9, 2, 0, -3]
    result = multithreaded_sort(input_list)
    expected = sorted(input_list)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ Test 8 passed: List with negative numbers")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING TEST SUITE FOR MULTITHREADED SORTING")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_case,
        test_already_sorted,
        test_reverse_sorted,
        test_duplicates,
        test_single_element,
        test_two_elements,
        test_large_random,
        test_negative_numbers,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} total")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed successfully!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
