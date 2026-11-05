# Arrays in Java

## What is an Array?

An array is a linear data structure that stores a fixed number of
elements of the same data type in contiguous memory locations.

In Java, arrays are objects. Their size is determined when they
are created and cannot be changed afterward.

## Declaration and Initialization

An integer array can be declared and initialized as follows:

int[] numbers = {10, 20, 30, 40, 50};

Alternatively:

int[] numbers = new int[5];

The second declaration creates an integer array of size 5.
Each element initially contains the default value 0.

## Accessing Elements

Array elements are accessed using zero-based indexing.

numbers[0] returns 10.
numbers[2] returns 30.

Accessing an index outside the valid range causes an
ArrayIndexOutOfBoundsException.

## Traversing an Array

A standard for loop can traverse an array:

for (int i = 0; i < numbers.length; i++) {
    System.out.println(numbers[i]);
}

The time complexity of traversing an array of n elements is O(n).

## Common Operations and Complexities

- Access by index: O(1)
- Linear search: O(n)
- Updating an element by index: O(1)
- Inserting into the middle: O(n), because elements may need shifting
- Deleting from the middle: O(n), because elements may need shifting

## Common Mistakes

1. Using an index equal to the array length.
2. Confusing array length with String length().
3. Assuming arrays automatically resize.
4. Using <= instead of < in a traversal loop.

## Example: Finding the Maximum Element

Initialize max with the first element.
Traverse the remaining elements.
Whenever an element is greater than max, update max.

The algorithm takes O(n) time and O(1) auxiliary space.