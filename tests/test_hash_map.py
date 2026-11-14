import string

import pytest
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, precondition, rule

from dsa import HashMap


def test_total_collision_still_correct() -> None:  # Review Focus 3
    m = HashMap[str, int](hash_fn=lambda k: 0)
    for i, k in enumerate("abcdefghij"):
        m[k] = i
    m["c"] = 100
    assert len(m) == 10
    assert m["c"] == 100
    del m["e"]
    assert "e" not in m
    with pytest.raises(KeyError):
        m["e"]
    with pytest.raises(KeyError):
        del m["e"]
    m["e"] = 42
    assert m["e"] == 42
    assert len(m) == 10


def test_resizes_past_three_quarters() -> None:
    m = HashMap[int, int]()
    assert m.capacity == 8
    for i in range(6):
        m[i] = i
    assert m.capacity == 8
    assert m.load_factor == 0.75
    m[6] = 6
    assert m.capacity == 16
    assert all(m[i] == i for i in range(7))


def test_fixed_table_buckets() -> None:
    m = HashMap[int, None](7, hash_fn=lambda x: x % 7, auto_resize=False)
    for k in [2341, 4234, 2839, 430, 22, 397, 3920]:
        m[k] = None
    assert m.buckets()[3] == [2341, 430]
    assert m.buckets()[2] == []
    assert m.bucket_index(430) == 3
    assert m.capacity == 7


def test_get_items_and_bad_capacity() -> None:
    m = HashMap[str, int]()
    m["a"] = 1
    assert m.get("a") == 1
    assert m.get("z") is None
    assert m.get("z", 0) == 0
    assert m.items() == [("a", 1)]
    assert list(m) == ["a"]
    with pytest.raises(ValueError):
        HashMap[str, int](0)


keys = st.integers() | st.text(alphabet=string.ascii_letters, max_size=3)


class HashMapVsDict(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.model: dict[int | str, int] = {}
        self.sut = HashMap[int | str, int]()

    @rule(k=keys, v=st.integers())
    def set(self, k: int | str, v: int) -> None:
        self.model[k] = v
        self.sut[k] = v

    @precondition(lambda self: len(self.model) > 0)
    @rule(data=st.data())
    def delete(self, data: st.DataObject) -> None:
        k = data.draw(st.sampled_from(sorted(self.model, key=repr)))
        del self.model[k]
        del self.sut[k]

    @rule(k=keys)
    def get(self, k: int | str) -> None:
        assert self.sut.get(k) == self.model.get(k)
        assert (k in self.sut) == (k in self.model)

    @invariant()
    def same_mapping(self) -> None:
        assert len(self.sut) == len(self.model)
        assert dict(self.sut.items()) == self.model
        assert self.sut.load_factor <= 0.75


TestHashMap = HashMapVsDict.TestCase
