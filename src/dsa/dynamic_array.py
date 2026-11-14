"""Sequential list backed by a fixed-size block that doubles when full."""

from collections.abc import Iterable, Iterator
from typing import cast

INITIAL_CAPACITY = 4


class DynamicArray[T]:
    """A growable array, like ``list``: O(1) amortized append, O(n) insert/remove in the middle.

    The raw storage is a fixed-size block; it is only ever indexed, never resized in place.
    """

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._data: list[T | None] = [None] * INITIAL_CAPACITY
        self._size = 0
        for item in items:
            self.append(item)

    @property
    def capacity(self) -> int:
        return len(self._data)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield cast(T, self._data[i])

    def __contains__(self, x: object) -> bool:
        return any(item == x for item in self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DynamicArray):
            return NotImplemented
        return len(self) == len(other) and all(a == b for a, b in zip(self, other, strict=True))

    def __repr__(self) -> str:
        return f"DynamicArray({list(self)!r})"

    def __getitem__(self, i: int) -> T:
        return cast(T, self._data[self._normalize(i)])

    def __setitem__(self, i: int, x: T) -> None:
        self._data[self._normalize(i)] = x

    def append(self, x: T) -> None:
        if self._size == self.capacity:
            self._grow()
        self._data[self._size] = x
        self._size += 1

    def insert(self, i: int, x: T) -> None:
        """Insert before index ``i``; like ``list.insert``, out-of-range indices clamp to the ends."""
        if i < 0:
            i = max(0, i + self._size)
        i = min(i, self._size)
        if self._size == self.capacity:
            self._grow()
        for j in range(self._size, i, -1):
            self._data[j] = self._data[j - 1]
        self._data[i] = x
        self._size += 1

    def pop(self, i: int = -1) -> T:
        if self._size == 0:
            raise IndexError("pop from empty array")
        i = self._normalize(i)
        item = cast(T, self._data[i])
        for j in range(i, self._size - 1):
            self._data[j] = self._data[j + 1]
        self._size -= 1
        self._data[self._size] = None  # drop the reference so it can be garbage-collected
        return item

    def remove(self, x: T) -> None:
        self.pop(self.index(x))

    def index(self, x: T) -> int:
        for i, item in enumerate(self):
            if item == x:
                return i
        raise ValueError(f"{x!r} is not in array")

    def _normalize(self, i: int) -> int:
        if i < 0:
            i += self._size
        if not 0 <= i < self._size:
            raise IndexError("array index out of range")
        return i

    def _grow(self) -> None:
        bigger: list[T | None] = [None] * (self.capacity * 2)
        for i in range(self._size):
            bigger[i] = self._data[i]
        self._data = bigger
