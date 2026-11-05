
# Binary Search in Java

## What Is Binary Search?

Binary search is an efficient searching algorithm used to find an element in a **sorted array**.

Instead of checking every element, it repeatedly divides the search interval in half.

## Iterative Binary Search

### Algorithm

1. Initialize `low = 0` and `high = arr.length - 1`.
2. Calculate the middle index: `mid = low + (high - low) / 2`.
3. If `arr[mid]` equals the target, return `mid`.
4. If the target is smaller, search the left half by setting `high = mid - 1`.
5. If the target is larger, search the right half by setting `low = mid + 1`.
6. Repeat while `low <= high`.
7. Return `-1` if the target is not found.

### Java Implementation

```java
int binarySearch(int[] arr, int target) {
    int low = 0;
    int high = arr.length - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return -1;
}
```

### Complexity

- Best case: O(1)
- Average case: O(log n)
- Worst case: O(log n)
- Auxiliary space: O(1)

## Recursive Binary Search

### Java Implementation

```java
int binarySearch(int[] arr, int low, int high, int target) {
    if (low > high) {
        return -1;
    }

    int mid = low + (high - low) / 2;

    if (arr[mid] == target) {
        return mid;
    }

    if (arr[mid] < target) {
        return binarySearch(arr, mid + 1, high, target);
    }

    return binarySearch(arr, low, mid - 1, target);
}
```

### Complexity

- Time: O(log n)
- Auxiliary space: O(log n) due to recursion stack.

## Finding the First Occurrence

When duplicates exist, binary search can be modified to find the first occurrence.

When the target is found, record the index and continue searching the left half.

## Finding the Last Occurrence

When the target is found, record the index and continue searching the right half.

## Binary Search on Answer

Binary search can also be applied to a range of possible answers when a monotonic condition exists.

Examples:
- Minimum capacity needed to ship packages within D days.
- Minimum eating speed to finish bananas within H hours.
- Minimum possible maximum workload.

## Common Mistakes

- Applying binary search to an unsorted array.
- Using `low < high` when `low <= high` is required.
- Forgetting to update `low` or `high`.
- Using `mid + 1` or `mid - 1` incorrectly.
- Calculating the midpoint as `(low + high) / 2`, which can overflow for very large indices.

## Important Interview Problems

- Binary Search
- Search Insert Position
- First and Last Position of Element in Sorted Array
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array
- Koko Eating Bananas
