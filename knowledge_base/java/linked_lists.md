# Linked Lists in Java

## What is a Linked List?

A linked list is a linear data structure consisting of nodes.
Each node stores data and a reference to the next node.

Unlike arrays, linked list elements are not required to occupy
contiguous memory locations.

A linked list can grow or shrink dynamically.

## Structure of a Node

A basic singly linked list node in Java can be represented as:

class Node {
    int data;
    Node next;

    Node(int data) {
        this.data = data;
        this.next = null;
    }
}

The data field stores the value.
The next field stores a reference to the next node.

The first node is called the head.
The last node points to null.

## Types of Linked Lists

### Singly Linked List

Each node contains data and a reference to the next node.

Traversal is possible only in the forward direction.

### Doubly Linked List

Each node contains:
- Data
- A reference to the next node
- A reference to the previous node

Traversal is possible in both directions.

### Circular Linked List

The last node points back to the first node instead of null.

Circular linked lists can be singly or doubly linked.

## Traversing a Singly Linked List

To traverse a linked list, start from the head and follow
the next references until reaching null.

Example:

Node current = head;

while (current != null) {
    System.out.println(current.data);
    current = current.next;
}

Time complexity: O(n)
Auxiliary space: O(1)

## Insertion Operations

### Insertion at the Beginning

Create a new node.
Set its next reference to the current head.
Update head to the new node.

Time complexity: O(1)

### Insertion at the End

Traverse to the last node.
Set its next reference to the new node.

Time complexity: O(n) without a tail reference.
Time complexity: O(1) with a maintained tail reference.

### Insertion at a Given Position

Traverse to the node immediately before the target position.
Adjust references to insert the new node.

Time complexity: O(n)

## Deletion Operations

### Deletion at the Beginning

Move head to head.next.

Time complexity: O(1)

### Deletion at the End

Traverse to the second-last node.
Set its next reference to null.

Time complexity: O(n) in a singly linked list.

### Deletion by Value

Search for the node containing the target value.
Adjust the previous node's next reference to skip the target node.

Time complexity: O(n)

## Reversing a Singly Linked List

A linked list can be reversed iteratively using three references:
- prev
- current
- nextNode

Algorithm:

1. Initialize prev to null.
2. Set current to head.
3. Store current.next in nextNode.
4. Reverse the current node's next reference to prev.
5. Move prev to current.
6. Move current to nextNode.
7. Repeat until current becomes null.
8. Update head to prev.

Java implementation:

Node reverseList(Node head) {
    Node prev = null;
    Node current = head;

    while (current != null) {
        Node nextNode = current.next;
        current.next = prev;
        prev = current;
        current = nextNode;
    }

    return prev;
}

Time complexity: O(n)
Auxiliary space: O(1)

## Detecting a Cycle in a Linked List

Floyd's Cycle Detection Algorithm uses two pointers:
- Slow pointer moves one node at a time.
- Fast pointer moves two nodes at a time.

If a cycle exists, the two pointers eventually meet.

If the fast pointer or fast.next becomes null,
the linked list does not contain a cycle.

Java implementation:

boolean hasCycle(Node head) {
    Node slow = head;
    Node fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;

        if (slow == fast) {
            return true;
        }
    }

    return false;
}

Time complexity: O(n)
Auxiliary space: O(1)

## Finding the Middle Node

Use the slow and fast pointer technique.

Slow moves one step at a time.
Fast moves two steps at a time.

When fast reaches the end, slow points to the middle.

Time complexity: O(n)
Auxiliary space: O(1)

For an even-length list, this implementation returns the
second middle node.

## Common Time Complexities

- Access by index: O(n)
- Search by value: O(n)
- Insertion at beginning: O(1)
- Deletion at beginning: O(1)
- Insertion at end: O(n) without a tail reference
- Traversal: O(n)
- Reversal: O(n)
- Cycle detection: O(n)

## Common Mistakes

1. Forgetting to update head after insertion or deletion.
2. Losing the remaining list by changing references in the wrong order.
3. Accessing current.next when current is null.
4. Forgetting to check fast.next before accessing fast.next.next.
5. Confusing node references with node values.
6. Creating an infinite loop while traversing a cyclic list.
7. Returning the old head instead of the new head after reversal.

## Important Interview Problems

- Reverse Linked List
- Linked List Cycle
- Linked List Cycle II
- Merge Two Sorted Lists
- Remove Nth Node From End of List
- Middle of the Linked List
- Palindrome Linked List
- Add Two Numbers
- Intersection of Two Linked Lists