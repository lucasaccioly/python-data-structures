"""Rectangular matrix of numbers, with the usual operations written as explicit loops."""

from collections.abc import Sequence


class Matrix:
    def __init__(self, rows: Sequence[Sequence[float]]) -> None:
        if not rows or not rows[0]:
            raise ValueError("a matrix needs at least one row and one column")
        width = len(rows[0])
        if any(len(r) != width for r in rows):
            raise ValueError("all rows must have the same length")
        self._rows = [list(r) for r in rows]  # copy, so the caller's lists can't change us

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._rows), len(self._rows[0])

    def __getitem__(self, rc: tuple[int, int]) -> float:
        r, c = rc
        return self._rows[r][c]

    def rows(self) -> list[list[float]]:
        return [list(r) for r in self._rows]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self._rows == other._rows

    def __repr__(self) -> str:
        return f"Matrix({self._rows!r})"

    def transpose(self) -> "Matrix":
        n, m = self.shape
        return Matrix([[self._rows[r][c] for r in range(n)] for c in range(m)])

    def __add__(self, other: "Matrix") -> "Matrix":
        if self.shape != other.shape:
            raise ValueError(f"cannot add {self.shape} and {other.shape}")
        n, m = self.shape
        return Matrix([[self._rows[r][c] + other._rows[r][c] for c in range(m)] for r in range(n)])

    def __matmul__(self, other: "Matrix") -> "Matrix":
        """O(n·m·p) for an n×m times m×p product."""
        n, m = self.shape
        m2, p = other.shape
        if m != m2:
            raise ValueError(f"cannot multiply {self.shape} by {other.shape}")
        result: list[list[float]] = []
        for r in range(n):
            row: list[float] = []
            for c in range(p):
                total: float = 0
                for k in range(m):
                    total += self._rows[r][k] * other._rows[k][c]
                row.append(total)
            result.append(row)
        return Matrix(result)

    def row_sums(self) -> list[float]:
        sums: list[float] = []
        for row in self._rows:
            total: float = 0
            for value in row:
                total += value
            sums.append(total)
        return sums

    def col_sums(self) -> list[float]:
        return self.transpose().row_sums()
