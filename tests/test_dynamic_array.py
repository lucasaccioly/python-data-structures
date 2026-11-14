import pytest
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, precondition, rule

from dsa import DynamicArray


def test_grows_by_doubling() -> None:
    a = DynamicArray[int]()
    assert a.capacity == 4
    for i in range(5):
        a.append(i)
    assert a.capacity == 8
    assert list(a) == [0, 1, 2, 3, 4]


def test_indices_like_list() -> None:
    a = DynamicArray([10, 20, 30])
    assert a[-1] == 30
    assert a[-3] == 10
    for bad in (3, -4):
        with pytest.raises(IndexError):
            a[bad]
    with pytest.raises(IndexError):
        DynamicArray[int]().pop()
    a.insert(99, 40)
    a.insert(-99, 0)
    assert list(a) == [0, 10, 20, 30, 40]
    with pytest.raises(ValueError):
        a.remove(7)


def test_index_contains_and_repr() -> None:
    a = DynamicArray("abc")
    assert a.index("c") == 2
    assert "b" in a
    assert "z" not in a
    assert repr(a) == "DynamicArray(['a', 'b', 'c'])"
    assert a == DynamicArray(["a", "b", "c"])
    with pytest.raises(ValueError):
        a.index("z")


class DynamicArrayVsList(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.model: list[int] = []
        self.sut = DynamicArray[int]()

    @rule(x=st.integers())
    def append(self, x: int) -> None:
        self.model.append(x)
        self.sut.append(x)

    @rule(i=st.integers(-20, 20), x=st.integers())
    def insert(self, i: int, x: int) -> None:
        self.model.insert(i, x)
        self.sut.insert(i, x)

    @precondition(lambda self: len(self.model) > 0)
    @rule(data=st.data())
    def pop(self, data: st.DataObject) -> None:
        n = len(self.model)
        i = data.draw(st.integers(-n, n - 1))
        assert self.sut.pop(i) == self.model.pop(i)

    @precondition(lambda self: len(self.model) > 0)
    @rule(data=st.data(), x=st.integers())
    def setitem(self, data: st.DataObject, x: int) -> None:
        n = len(self.model)
        i = data.draw(st.integers(-n, n - 1))
        self.model[i] = x
        self.sut[i] = x

    @precondition(lambda self: len(self.model) > 0)
    @rule(data=st.data())
    def remove(self, data: st.DataObject) -> None:
        x = data.draw(st.sampled_from(self.model))
        self.model.remove(x)
        self.sut.remove(x)

    @invariant()
    def same_contents(self) -> None:
        assert len(self.sut) == len(self.model)
        assert list(self.sut) == self.model


TestDynamicArray = DynamicArrayVsList.TestCase
