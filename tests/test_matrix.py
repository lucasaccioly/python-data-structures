import pytest
from hypothesis import given
from hypothesis import strategies as st

from dsa import Matrix


def test_multiply_add_transpose() -> None:
    a = Matrix([[1, 2], [3, 4]])
    assert a @ Matrix([[5, 6], [7, 8]]) == Matrix([[19, 22], [43, 50]])
    assert a + a == Matrix([[2, 4], [6, 8]])
    t = Matrix([[1, 2, 3], [4, 5, 6]]).transpose()
    assert t.shape == (3, 2)
    assert t == Matrix([[1, 4], [2, 5], [3, 6]])
    assert t[2, 1] == 6
    assert repr(a) == "Matrix([[1, 2], [3, 4]])"


def test_sums() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.row_sums() == [6, 15]
    assert m.col_sums() == [5, 7, 9]


def test_rows_is_a_copy() -> None:
    source = [[1, 2], [3, 4]]
    m = Matrix(source)
    source[0][0] = 99
    m.rows()[0][0] = 99
    assert m[0, 0] == 1


@pytest.mark.parametrize("rows", [[], [[]], [[1, 2], [3]]])
def test_invalid_shapes_raise(rows: list[list[float]]) -> None:  # Review Focus 5
    with pytest.raises(ValueError):
        Matrix(rows)


def test_mismatched_operations_raise() -> None:  # Review Focus 5
    a, b = Matrix([[1, 2]]), Matrix([[1], [2], [3]])
    with pytest.raises(ValueError):
        a + b
    with pytest.raises(ValueError):
        a @ b


matrices = st.integers(1, 5).flatmap(
    lambda cols: st.lists(
        st.lists(st.integers(-100, 100), min_size=cols, max_size=cols), min_size=1, max_size=5
    )
)


@given(rows=matrices)
def test_properties(rows: list[list[int]]) -> None:
    m = Matrix(rows)
    assert m.transpose().transpose() == m
    assert m.row_sums() == [sum(r) for r in rows]
    assert m.col_sums() == [sum(c) for c in zip(*rows, strict=True)]
    assert m.rows() == rows
