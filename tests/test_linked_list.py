from collections import deque

import pytest
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, precondition, rule

from dsa import LinkedList


def test_remove_middle_keeps_links() -> None:
    ll = LinkedList([1, 2, 3])
    ll.remove(2)
    assert list(ll) == [1, 3]
    assert list(reversed(ll)) == [3, 1]
    assert repr(ll) == "LinkedList([1, 3])"


def test_pop_empty_raises() -> None:
    for pop in (LinkedList[int]().pop, LinkedList[int]().popleft):
        with pytest.raises(IndexError):
            pop()
    with pytest.raises(ValueError):
        LinkedList([1]).remove(2)


class LinkedListVsDeque(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.model: deque[int] = deque()
        self.sut = LinkedList[int]()

    @rule(x=st.integers(0, 5))
    def append(self, x: int) -> None:
        self.model.append(x)
        self.sut.append(x)

    @rule(x=st.integers(0, 5))
    def appendleft(self, x: int) -> None:
        self.model.appendleft(x)
        self.sut.appendleft(x)

    @precondition(lambda self: len(self.model) > 0)
    @rule()
    def pop(self) -> None:
        assert self.sut.pop() == self.model.pop()

    @precondition(lambda self: len(self.model) > 0)
    @rule()
    def popleft(self) -> None:
        assert self.sut.popleft() == self.model.popleft()

    @precondition(lambda self: len(self.model) > 0)
    @rule(data=st.data())
    def remove(self, data: st.DataObject) -> None:
        x = data.draw(st.sampled_from(list(self.model)))
        self.model.remove(x)
        self.sut.remove(x)

    @invariant()
    def same_both_ways(self) -> None:
        assert len(self.sut) == len(self.model)
        assert list(self.sut) == list(self.model)
        assert list(reversed(self.sut)) == list(reversed(self.model))
        assert all(x in self.sut for x in self.model)


TestLinkedList = LinkedListVsDeque.TestCase
