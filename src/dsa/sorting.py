"""Five classic sorting algorithms.

Every function takes any iterable, returns a new list and leaves the input alone. ``reverse=True``
sorts in descending order; the stable algorithms (insertion and merge) stay stable either way,
like ``sorted``. Items only need ``<``.
"""

import random
from collections.abc import Callable, Iterable
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def _before[CT: Comparable](reverse: bool) -> Callable[[CT, CT], bool]:
    """Strict "must come before" for the requested order; equal items never come before each other."""
    if reverse:
        return lambda a, b: b < a
    return lambda a, b: a < b


def selection_sort[CT: Comparable](items: Iterable[CT], *, reverse: bool = False) -> list[CT]:
    """O(n²) always: find the smallest remaining item and swap it into place. Not stable."""
    a = list(items)
    before: Callable[[CT, CT], bool] = _before(reverse)
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            if before(a[j], a[m]):
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def insertion_sort[CT: Comparable](items: Iterable[CT], *, reverse: bool = False) -> list[CT]:
    """O(n²) worst, O(n) on sorted input: grow a sorted prefix one item at a time. Stable."""
    a = list(items)
    before: Callable[[CT, CT], bool] = _before(reverse)
    for i in range(1, len(a)):
        item, j = a[i], i - 1
        while j >= 0 and before(item, a[j]):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = item
    return a


def merge_sort[CT: Comparable](items: Iterable[CT], *, reverse: bool = False) -> list[CT]:
    """O(n log n) always, O(n) extra space: sort each half, then merge them. Stable."""
    before: Callable[[CT, CT], bool] = _before(reverse)

    def sort(a: list[CT]) -> list[CT]:
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left, right = sort(a[:mid]), sort(a[mid:])
        merged: list[CT] = []
        i = j = 0
        while i < len(left) and j < len(right):
            # take from the right only when strictly before: ties keep their original order
            if before(right[j], left[i]):
                merged.append(right[j])
                j += 1
            else:
                merged.append(left[i])
                i += 1
        return merged + left[i:] + right[j:]

    return sort(list(items))


def quick_sort[CT: Comparable](items: Iterable[CT], *, reverse: bool = False) -> list[CT]:
    """O(n log n) expected, O(n²) worst (vanishingly unlikely with a random pivot). Not stable.

    A random pivot avoids the classic O(n²) on already-sorted input, and the three-way partition
    (before / equal / after) handles many duplicates in one pass. Recursing only into the smaller
    side keeps the stack depth at O(log n), so large inputs never hit ``RecursionError``.
    """
    a = list(items)
    before: Callable[[CT, CT], bool] = _before(reverse)

    def sort(lo: int, hi: int) -> None:  # sorts a[lo:hi]
        while hi - lo > 1:
            pivot = a[random.randrange(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i < gt:
                if before(a[i], pivot):
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif before(pivot, a[i]):
                    gt -= 1
                    a[gt], a[i] = a[i], a[gt]
                else:
                    i += 1
            if lt - lo < hi - gt:
                sort(lo, lt)
                lo = gt
            else:
                sort(gt, hi)
                hi = lt

    sort(0, len(a))
    return a


def heap_sort[CT: Comparable](items: Iterable[CT], *, reverse: bool = False) -> list[CT]:
    """O(n log n) always, O(1) extra space: build a heap, then move its top to the end. Not stable."""
    a = list(items)
    before: Callable[[CT, CT], bool] = _before(reverse)

    def sift_down(root: int, end: int) -> None:
        while (child := 2 * root + 1) < end:
            if child + 1 < end and before(a[child], a[child + 1]):
                child += 1
            if not before(a[root], a[child]):
                return
            a[root], a[child] = a[child], a[root]
            root = child

    for root in range(len(a) // 2 - 1, -1, -1):
        sift_down(root, len(a))
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a


ALGORITHMS: dict[str, Callable[..., list[Any]]] = {
    "selection_sort": selection_sort,
    "insertion_sort": insertion_sort,
    "merge_sort": merge_sort,
    "quick_sort": quick_sort,
    "heap_sort": heap_sort,
}
