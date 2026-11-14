"""Doubly linked list: O(1) at both ends, O(n) search."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass


@dataclass(slots=True, eq=False)
class _Node[T]:
    value: T
    prev: "_Node[T] | None" = None
    next: "_Node[T] | None" = None


class LinkedList[T]:
    """Nodes linked in both directions, so either end can be added to or removed in constant time."""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._head: _Node[T] | None = None
        self._tail: _Node[T] | None = None
        self._size = 0
        for item in items:
            self.append(item)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def __reversed__(self) -> Iterator[T]:
        node = self._tail
        while node is not None:
            yield node.value
            node = node.prev

    def __contains__(self, x: object) -> bool:
        return any(item == x for item in self)

    def __repr__(self) -> str:
        return f"LinkedList({list(self)!r})"

    def append(self, x: T) -> None:
        node = _Node(x, prev=self._tail)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def appendleft(self, x: T) -> None:
        node = _Node(x, next=self._head)
        if self._head is None:
            self._tail = node
        else:
            self._head.prev = node
        self._head = node
        self._size += 1

    def pop(self) -> T:
        if self._tail is None:
            raise IndexError("pop from empty list")
        node = self._tail
        self._unlink(node)
        return node.value

    def popleft(self) -> T:
        if self._head is None:
            raise IndexError("pop from empty list")
        node = self._head
        self._unlink(node)
        return node.value

    def remove(self, x: T) -> None:
        """Remove the first occurrence of ``x``."""
        node = self._head
        while node is not None:
            if node.value == x:
                self._unlink(node)
                return
            node = node.next
        raise ValueError(f"{x!r} is not in list")

    def _unlink(self, node: _Node[T]) -> None:
        if node.prev is None:
            self._head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self._tail = node.prev
        else:
            node.next.prev = node.prev
        node.prev = node.next = None
        self._size -= 1
