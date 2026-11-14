import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from dsa.sorting import ALGORITHMS, heap_sort, insertion_sort, merge_sort, quick_sort

Sort = Callable[..., list[Any]]


@pytest.mark.parametrize("sort", ALGORITHMS.values(), ids=ALGORITHMS.keys())
@given(xs=st.lists(st.integers()))
def test_matches_sorted(sort: Sort, xs: list[int]) -> None:
    original = list(xs)
    assert sort(xs) == sorted(xs)
    assert sort(xs, reverse=True) == sorted(xs, reverse=True)
    assert xs == original  # input untouched


def test_accepts_any_iterable() -> None:
    for sort in ALGORITHMS.values():
        assert sort(iter("banana")) == list("aaabnn")


@pytest.mark.parametrize("sort", [quick_sort, merge_sort, heap_sort])
def test_large_sorted_and_equal_inputs(sort: Sort) -> None:  # Review Focus 1
    start = time.perf_counter()
    for data in (list(range(10_000)), [7] * 10_000, list(range(10_000, 0, -1))):
        assert sort(data) == sorted(data)
    assert time.perf_counter() - start < 2


@dataclass
class Record:
    key: int
    tag: str

    def __lt__(self, other: "Record") -> bool:
        return self.key < other.key


@pytest.mark.parametrize("sort", [merge_sort, insertion_sort])
def test_stable(sort: Sort) -> None:
    records = [Record(2, "a"), Record(1, "b"), Record(2, "c"), Record(1, "d"), Record(2, "e")]
    assert [r.tag for r in sort(records)] == ["b", "d", "a", "c", "e"]
    assert [r.tag for r in sort(records, reverse=True)] == ["a", "c", "e", "b", "d"]
