"""LIFO stack on top of DynamicArray: push and pop work at the end, so both are O(1) amortized."""

from collections.abc import Iterator

from dsa.dynamic_array import DynamicArray


class Stack[T]:
    def __init__(self) -> None:
        self._items = DynamicArray[T]()

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return len(self._items) > 0

    def __iter__(self) -> Iterator[T]:
        """Iterate from the top of the stack down."""
        for i in range(len(self._items) - 1, -1, -1):
            yield self._items[i]

    def __repr__(self) -> str:
        return f"Stack(top={list(self)!r})"

    def push(self, x: T) -> None:
        self._items.append(x)

    def pop(self) -> T:
        if not self:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self:
            raise IndexError("peek at empty stack")
        return self._items[-1]
