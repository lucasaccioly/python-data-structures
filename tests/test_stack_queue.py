from collections import deque

import pytest
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, precondition, rule

from dsa import Queue, Stack


def test_stack_is_lifo() -> None:
    s = Stack[str]()
    assert not s
    for x in "abc":
        s.push(x)
    assert len(s) == 3
    assert s.peek() == "c"
    assert list(s) == ["c", "b", "a"]  # top to bottom
    assert [s.pop(), s.pop(), s.pop()] == ["c", "b", "a"]
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()


def test_empty_queue_raises() -> None:
    q = Queue[int]()
    assert not q
    for op in (q.dequeue, q.peek, q.peek_last):
        with pytest.raises(IndexError):
            op()


def test_queue_grows_after_wraparound() -> None:  # Review Focus 4
    q = Queue[int]()
    for i in range(4):
        q.enqueue(i)
    assert q.dequeue() == 0
    assert q.dequeue() == 1  # head now at 2
    for i in range(4, 9):
        q.enqueue(i)  # wraps around the end of the buffer, then grows
    assert list(q) == [2, 3, 4, 5, 6, 7, 8]
    assert q.peek() == 2
    assert q.peek_last() == 8
    assert len(q) == 7


class QueueVsDeque(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.model: deque[int] = deque()
        self.sut = Queue[int]()

    @rule(x=st.integers())
    def enqueue(self, x: int) -> None:
        self.model.append(x)
        self.sut.enqueue(x)

    @precondition(lambda self: len(self.model) > 0)
    @rule()
    def dequeue(self) -> None:
        assert self.sut.dequeue() == self.model.popleft()

    @precondition(lambda self: len(self.model) > 0)
    @rule()
    def peeks(self) -> None:
        assert self.sut.peek() == self.model[0]
        assert self.sut.peek_last() == self.model[-1]

    @invariant()
    def same_order(self) -> None:
        assert len(self.sut) == len(self.model)
        assert list(self.sut) == list(self.model)


TestQueue = QueueVsDeque.TestCase
