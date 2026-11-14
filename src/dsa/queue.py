"""FIFO queue on a circular buffer.

``list.pop(0)`` shifts every remaining element, so a list-based queue dequeues in O(n). Here the
front just moves forward (``head``) and wraps around the end of the block, so dequeue is O(1).
"""

from collections.abc import Iterator
from typing import cast

INITIAL_CAPACITY = 4


class Queue[T]:
    def __init__(self) -> None:
        self._data: list[T | None] = [None] * INITIAL_CAPACITY
        self._head = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def __iter__(self) -> Iterator[T]:
        """Iterate from the front (next to leave) to the back."""
        for i in range(self._size):
            yield cast(T, self._data[(self._head + i) % len(self._data)])

    def __repr__(self) -> str:
        return f"Queue(front={list(self)!r})"

    def enqueue(self, x: T) -> None:
        if self._size == len(self._data):
            self._grow()
        self._data[(self._head + self._size) % len(self._data)] = x
        self._size += 1

    def dequeue(self) -> T:
        if not self._size:
            raise IndexError("dequeue from empty queue")
        item = cast(T, self._data[self._head])
        self._data[self._head] = None  # drop the reference so it can be garbage-collected
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return item

    def peek(self) -> T:
        """The front item, the next one to be dequeued."""
        if not self._size:
            raise IndexError("peek at empty queue")
        return cast(T, self._data[self._head])

    def peek_last(self) -> T:
        """The back item, the most recently enqueued one."""
        if not self._size:
            raise IndexError("peek at empty queue")
        return cast(T, self._data[(self._head + self._size - 1) % len(self._data)])

    def _grow(self) -> None:
        # unroll the ring in order so the copy starts at index 0 again
        bigger: list[T | None] = [None] * (len(self._data) * 2)
        for i, item in enumerate(self):
            bigger[i] = item
        self._data = bigger
        self._head = 0
