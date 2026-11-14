"""Hash table with separate chaining.

Each bucket holds the ``(key, value)`` pairs whose hash lands on it. When more than 3/4 of the
capacity is used, the table doubles and every entry is rehashed, which keeps the chains short and
lookups O(1) on average. Doubling makes the rehash cost O(1) amortized per insert.
"""

from collections.abc import Callable, Hashable, Iterator
from typing import overload

MAX_LOAD_FACTOR = 0.75


class HashMap[K: Hashable, V]:
    def __init__(
        self,
        capacity: int = 8,
        *,
        hash_fn: Callable[[K], int] = hash,
        auto_resize: bool = True,
    ) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._hash_fn = hash_fn
        self._auto_resize = auto_resize
        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(capacity)]
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._buckets)

    @property
    def load_factor(self) -> float:
        return self._size / self.capacity

    def bucket_index(self, key: K) -> int:
        return self._hash_fn(key) % self.capacity

    def buckets(self) -> list[list[K]]:
        """The keys in each bucket, in insertion order; useful to see collisions."""
        return [[k for k, _ in bucket] for bucket in self._buckets]

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def __contains__(self, key: object) -> bool:
        try:
            self[key]  # type: ignore[index]
        except KeyError:
            return False
        return True

    def __repr__(self) -> str:
        return f"HashMap({dict(self.items())!r})"

    def items(self) -> list[tuple[K, V]]:
        return [pair for bucket in self._buckets for pair in bucket]

    def __getitem__(self, key: K) -> V:
        for k, v in self._buckets[self.bucket_index(key)]:
            if k == key:
                return v
        raise KeyError(key)

    @overload
    def get(self, key: K) -> V | None: ...
    @overload
    def get[D](self, key: K, default: D) -> V | D: ...
    def get(self, key: K, default: object = None) -> object:
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key: K, value: V) -> None:
        bucket = self._buckets[self.bucket_index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._auto_resize and self.load_factor > MAX_LOAD_FACTOR:
            self._resize(self.capacity * 2)

    def __delitem__(self, key: K) -> None:
        bucket = self._buckets[self.bucket_index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def _resize(self, capacity: int) -> None:
        old = self.items()
        self._buckets = [[] for _ in range(capacity)]
        for k, v in old:
            self._buckets[self.bucket_index(k)].append((k, v))
