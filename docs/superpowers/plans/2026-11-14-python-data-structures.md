# python-data-structures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A public, zero-dependency Python package `dsa` with seven from-scratch data structures and five sorts. It is tested against the built-ins with Hypothesis, and the old college exercises are rewritten as tested examples.

**Architecture:**
- The package uses a `src/` layout: `src/dsa/`, one module per structure. `Stack` is built on `DynamicArray`, and the examples are built on the package.
- `examples/` is a top-level package. Each example module has pure functions that the tests import, plus a `main()` that prints pt-BR output; run one with `python -m examples.<name>`.
- Property tests compare each structure with `list`, `collections.deque`, `dict` or `sorted` through Hypothesis stateful machines.

**Tech Stack:** Python ≥3.12, pytest, Hypothesis, ruff, mypy `--strict`, hatchling, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-14-python-data-structures-design.md`

## Global Constraints

- The package has zero runtime dependencies. Dev dependencies, in the `[dev]` extra: `pytest`, `hypothesis`, `ruff`, `mypy`.
- `requires-python = ">=3.12"`. CI runs a matrix on 3.12 and 3.14.
- Code, identifiers, docstrings and commits are in English. README and the example `main()` output are in pt-BR.
- No structure may wrap its built-in equivalent:
  - `DynamicArray` may use a fixed-size Python list (`[None] * capacity`) as raw storage, and only index it. No `append`, `insert` or `pop` on it.
  - `LinkedList` uses nodes.
  - `HashMap` uses buckets as Python lists of `(key, value)` tuples. It does not use a `dict`.
- Errors match the built-ins:
  - `IndexError` for bad indices and for pop/peek on an empty structure.
  - `KeyError` for missing keys.
  - `ValueError` for a value that is missing or invalid.
- Every public class and function has type hints and passes `mypy --strict`. Tests are type-checked too: test functions are annotated `-> None`. The test snippets below are shorthand: ruff format splits their `;` onto separate lines.
- No college or employer name anywhere. Example data is neutral (documents, customers, pages).
- The license is MIT, "Copyright (c) 2026 Lucas Accioly".
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **Quick sort on already-sorted or all-equal input of 10 000 items** must not raise `RecursionError` and must stay fast. Test: Task 5.
2. **`DynamicArray` indices:** negative and out-of-range indices must behave like `list`, raising `IndexError`. This covers `pop()` on an empty array and `insert` beyond the end, which appends like `list.insert`. Test: Task 1.
3. **`HashMap` under total collision** (`hash_fn=lambda k: 0`) must stay correct. Overwriting a key must not change `len`, and delete followed by reinsert must work. Test: Task 4.
4. **`Queue` growth while the ring has wrapped** (head ≠ 0) must preserve FIFO order. Test: Task 3.
5. **Invalid input:** a ragged or empty `Matrix`, mismatched shapes for `+` and `@`, and malformed RPN (`"3 +"`, `"1 2"`, `"2 x 3"`) must raise `ValueError`, not crash with another error. Test: Task 6 and Task 7.

---

### Task 1: Scaffold + DynamicArray

**Files:**
- Create the project files:
  - `pyproject.toml`
  - `.gitignore` (covering `.venv/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.hypothesis/`, `dist/`, `.superpowers/`)
  - `LICENSE`
  - `.github/workflows/ci.yml`
  - `src/dsa/__init__.py`
  - `src/dsa/py.typed`
  - `src/dsa/dynamic_array.py`
- Test: `tests/test_dynamic_array.py`

**Interfaces:**
- Produces: `class DynamicArray(Generic[T])` with the following:
  - `__init__(self, items: Iterable[T] = ())`
  - `append(x: T) -> None`
  - `insert(i: int, x: T) -> None`, with `list.insert` semantics: clamps the index and accepts negatives.
  - `pop(i: int = -1) -> T`
  - `remove(x: T) -> None`, raising `ValueError`.
  - `index(x: T) -> int`, raising `ValueError`.
  - `__getitem__(i: int) -> T` and `__setitem__(i: int, x: T) -> None`. These take an int only (no slices) and support negative indices.
  - `__len__`, `__iter__`, `__contains__`, `__eq__` (against another `DynamicArray`), and `__repr__` as `DynamicArray([1, 2])`.
  - The `capacity: int` property.
  - Initial capacity is 4. Capacity doubles when full and never shrinks.
- `dsa/__init__.py` re-exports every public name and keeps an `__all__`. Later tasks add their names to it.

**Steps:**

- [ ] **Step 1: Write the scaffold files**
  - `pyproject.toml`:
    - `[build-system]`: hatchling.
    - `[project]`: name `python-data-structures`, version `1.0.0`, description, `requires-python>=3.12`, MIT license, `dependencies = []`.
    - `[project.optional-dependencies] dev = ["pytest", "hypothesis", "ruff", "mypy"]`.
    - `[tool.hatch.build.targets.wheel] packages = ["src/dsa"]`.
    - `[tool.pytest.ini_options] pythonpath = [".", "src"]`, `testpaths = ["tests"]`.
    - `[tool.ruff] line-length = 110`, `[tool.ruff.lint] select = ["E","F","I","UP","B","SIM"]`.
    - `[tool.mypy] strict = true`, `files = ["src", "examples", "tests"]`, `mypy_path = "src"`.
  - CI: on push and PR, a matrix of `python-version: ["3.12", "3.14"]`. It runs `pip install -e ".[dev]"`, then `ruff check .`, `ruff format --check .`, `mypy`, and `pytest -q`.
  - Local venv: `python -m venv .venv && .venv/Scripts/pip install -e ".[dev]"`.

- [ ] **Step 2: Write the failing tests** in `tests/test_dynamic_array.py`

```python
def test_grows_by_doubling():
    a = DynamicArray[int]()
    assert a.capacity == 4
    for i in range(5):
        a.append(i)
    assert a.capacity == 8 and list(a) == [0, 1, 2, 3, 4]

def test_indices_like_list():  # Review Focus 2
    a = DynamicArray([10, 20, 30])
    assert a[-1] == 30 and a[-3] == 10
    for bad in (3, -4):
        with pytest.raises(IndexError):
            a[bad]
    with pytest.raises(IndexError):
        DynamicArray[int]().pop()
    a.insert(99, 40); a.insert(-99, 0)
    assert list(a) == [0, 10, 20, 30, 40]
    with pytest.raises(ValueError):
        a.remove(7)
```

  Plus `class DynamicArrayVsList(RuleBasedStateMachine)`:
  - Rules: `append`, `insert(i in -20..20)`, `pop` (when non-empty, `i` within range), `setitem`, and `remove` of an existing value.
  - Invariant: `list(model) == list(sut)` and `len` matches.
  - Hook it up with `TestDynamicArray = DynamicArrayVsList.TestCase`.

- [ ] **Step 3: Run** `.venv/Scripts/pytest tests/test_dynamic_array.py -q`. Expected: it fails with an ImportError.
- [ ] **Step 4: Implement** `DynamicArray` in `src/dsa/dynamic_array.py`. Storage is a `[None] * capacity` list plus a size counter. Elements shift by index loops.
- [ ] **Step 5: Run** `pytest -q && ruff check . && ruff format --check . && mypy`. Expected: all green.
- [ ] **Step 6: Commit** with the message `feat: scaffold project and DynamicArray`.

### Task 2: LinkedList

**Files:** Create `src/dsa/linked_list.py`. Test: `tests/test_linked_list.py`.

**Interfaces:**
- Produces: `class LinkedList(Generic[T])`, doubly linked with `head` and `tail` nodes, with the following:
  - `__init__(items: Iterable[T] = ())`
  - `append(x)` and `appendleft(x)`
  - `pop() -> T` and `popleft() -> T`, raising `IndexError("pop from empty list")`.
  - `remove(x) -> None`, removing the first occurrence and raising `ValueError`.
  - `__len__`, `__iter__`, `__reversed__`, `__contains__`, and `__repr__` as `LinkedList([1, 2])`.

**Steps:**

- [ ] **Step 1: Write the failing tests:**
  - `test_remove_middle_keeps_links`: in `LinkedList([1,2,3])`, removing 2 leaves `list(ll) == [1,3]` and `list(reversed(ll)) == [3,1]`.
  - `test_pop_empty_raises`.
  - A Hypothesis `RuleBasedStateMachine` against `collections.deque`, with all six mutators. Its invariant checks forward and reversed iteration, so it catches a broken `prev` pointer.
- [ ] **Step 2: Run.** Expected: it fails.
- [ ] **Step 3: Implement**, using a `_Node` dataclass with `__slots__` and the fields `value`, `prev`, `next`.
- [ ] **Step 4: Run** the full check from Task 1 Step 5. Expected: green.
- [ ] **Step 5: Commit** with the message `feat: add doubly linked list`.

### Task 3: Stack and Queue

**Files:** Create `src/dsa/stack.py` and `src/dsa/queue.py`. Test: `tests/test_stack_queue.py`.

**Interfaces:**
- Consumes: `DynamicArray`, from Task 1.
- Produces:
  - `class Stack(Generic[T])`:
    - `push(x) -> None`
    - `pop() -> T`, raising `IndexError("pop from empty stack")`.
    - `peek() -> T`, raising `IndexError`.
    - `__len__`, `__bool__`, and `__iter__` from top to bottom.
    - Backed by `DynamicArray`.
  - `class Queue(Generic[T])`, a ring buffer:
    - `enqueue(x) -> None`
    - `dequeue() -> T`, raising `IndexError("dequeue from empty queue")`.
    - `peek() -> T` for the front and `peek_last() -> T` for the back, both raising `IndexError` when empty.
    - `__len__`, `__bool__`, and `__iter__` from front to back.
    - Storage is `[None] * capacity` with `head` and `size`. Initial capacity is 4, and it doubles by copying the elements in order, starting from `head`.

**Steps:**

- [ ] **Step 1: Write the failing tests**

```python
def test_queue_grows_after_wraparound():  # Review Focus 4
    q = Queue[int]()
    for i in range(4): q.enqueue(i)
    assert q.dequeue() == 0 and q.dequeue() == 1      # head now at 2
    for i in range(4, 9): q.enqueue(i)                # wraps, then grows
    assert list(q) == [2, 3, 4, 5, 6, 7, 8]
    assert q.peek() == 2 and q.peek_last() == 8
```

  Plus stack LIFO and empty-error tests, and a Hypothesis state machine comparing `Queue` with `deque` (enqueue, dequeue, peek, peek_last).
- [ ] **Step 2: Run.** Expected: it fails.
- [ ] **Step 3: Implement** both classes.
- [ ] **Step 4: Run** the full check. Expected: green.
- [ ] **Step 5: Commit** with the message `feat: add stack and ring-buffer queue`.

### Task 4: HashMap

**Files:** Create `src/dsa/hash_map.py`. Test: `tests/test_hash_map.py`.

**Interfaces:**
- Produces: `class HashMap(Generic[K, V])` with the following:
  - `__init__(self, capacity: int = 8, *, hash_fn: Callable[[K], int] = hash, auto_resize: bool = True)`. Raises `ValueError` if `capacity < 1`.
  - `__setitem__`, plus `__getitem__` and `__delitem__`, which raise `KeyError(key)`.
  - `get(key, default=None)`, `__contains__`, `__len__`, `__iter__` over keys, and `items() -> list[tuple[K, V]]`.
  - `bucket_index(key) -> int`, computed as `hash_fn(key) % capacity`.
  - `buckets() -> list[list[K]]`, the keys per bucket, used by the collision example.
  - `capacity` and `load_factor` properties.
  - The load factor is `len / capacity`. When it would exceed `0.75` after an insert and `auto_resize` is set, capacity doubles and every entry is rehashed.

**Steps:**

- [ ] **Step 1: Write the failing tests:**
  - `test_total_collision_still_correct` (Review Focus 3):
    - With `HashMap[str, int](hash_fn=lambda k: 0)`, insert `"a".."j"`.
    - Overwrite `"c"`; `len` stays 10.
    - Delete `"e"`; `"e" not in m`, and `m["e"]` raises `KeyError`.
    - Reinsert `"e"`; `m["e"]` returns the new value.
  - `test_resizes_past_three_quarters`: with capacity 8, after 6 inserts the capacity is 8. After the 7th insert it is 16, and every key is still readable.
  - `test_fixed_table_buckets`: `HashMap[int, None](7, hash_fn=lambda x: x % 7, auto_resize=False)` filled with `[2341, 4234, 2839, 430, 22, 397, 3920]` gives `buckets()[3] == [2341, 430]` and `buckets()[2] == []`.
  - A Hypothesis state machine against `dict` with set, delete-existing, and get. Keys come from `st.integers() | st.text(max_size=3)`.
- [ ] **Step 2: Run.** Expected: it fails.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** the full check. Expected: green.
- [ ] **Step 5: Commit** with the message `feat: add hash map with chaining and resize`.

### Task 5: Sorting

**Files:** Create `src/dsa/sorting.py`. Test: `tests/test_sorting.py`.

**Interfaces:**
- Produces five functions, each with the signature `(items: Iterable[CT], *, reverse: bool = False) -> list[CT]`:
  - `selection_sort`
  - `insertion_sort`
  - `merge_sort`
  - `quick_sort`
  - `heap_sort`
- `CT` is a TypeVar bound to a `Comparable` Protocol that has `__lt__`.
- Each function returns a new list and does not mutate its input. `reverse=True` gives descending order.
- `ALGORITHMS: dict[str, Callable[..., list[Any]]]` maps each name to its function, for parametrized tests and the README.
- `quick_sort` uses a random pivot with a three-way partition (`<`, `==`, `>`). It recurses on the smaller side and loops on the larger side, so recursion depth is O(log n).
- `merge_sort` and `insertion_sort` are stable.

**Steps:**

- [ ] **Step 1: Write the failing tests**, parametrized over `ALGORITHMS`:
  - `@given(st.lists(st.integers()))`: `sort(xs) == sorted(xs)` and `sort(xs, reverse=True) == sorted(xs, reverse=True)`; the input list is unchanged.
  - `test_large_sorted_and_equal_inputs` (Review Focus 1), for `quick_sort`, `merge_sort` and `heap_sort` only: `range(10_000)`, then `[7] * 10_000`, then `range(10_000, 0, -1)`. Each result equals `sorted(...)`.
  - `test_stable`: `merge_sort` and `insertion_sort` sort `(key, tag)` records by key and keep the tag order. Use a small dataclass with `__lt__` comparing only the key.
- [ ] **Step 2: Run.** Expected: it fails.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** the full check. Expected: green, with the large-input test under 2 s.
- [ ] **Step 5: Commit** with the message `feat: add five sorting algorithms`.

### Task 6: Matrix

**Files:** Create `src/dsa/matrix.py`. Test: `tests/test_matrix.py`.

**Interfaces:**
- Produces: `class Matrix` with the following:
  - `__init__(self, rows: Sequence[Sequence[float]])`. Raises `ValueError` when the input is empty, has zero columns, or is ragged. It copies the input.
  - The `shape -> tuple[int, int]` property.
  - `__getitem__(self, rc: tuple[int, int]) -> float`.
  - `rows() -> list[list[float]]`, returning a copy.
  - `transpose() -> Matrix`.
  - `__add__(other: Matrix) -> Matrix` and `__matmul__(other: Matrix) -> Matrix`. Both raise `ValueError` on a shape mismatch and are written with explicit loops.
  - `row_sums() -> list[float]` and `col_sums() -> list[float]`.
  - `__eq__` and `__repr__`.

**Steps:**

- [ ] **Step 1: Write the failing tests:**
  - `Matrix([[1,2],[3,4]]) @ Matrix([[5,6],[7,8]]) == Matrix([[19,22],[43,50]])`.
  - Transpose of a 2×3 matrix gives a 3×2 matrix.
  - The `ValueError` cases (Review Focus 5): `Matrix([])`, `Matrix([[]])`, `Matrix([[1,2],[3]])`, `+` with different shapes, and `@` with inner dimensions that don't match.
  - `@given`: for random rectangular int matrices, `(a.transpose()).transpose() == a`, and `a.row_sums()` equals the Python sums.
- [ ] **Step 2: Run.** Expected: it fails.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** the full check. Expected: green.
- [ ] **Step 5: Commit** with the message `feat: add matrix`.

### Task 7: Examples (the original exercises)

**Files:**
- Create `examples/__init__.py` and these modules:
  - `examples/print_queue.py`
  - `examples/browser_history.py`
  - `examples/rpn.py`
  - `examples/expression.py`
  - `examples/undo_redo.py`
  - `examples/palindrome.py`
  - `examples/hash_collisions.py`
  - `examples/array_stats.py`
  - `examples/sleep_matrix.py`
- Test: `tests/test_examples.py`

**Interfaces:**
- Consumes: everything in `dsa`.
- Each module has a `main() -> None` that prints a short pt-BR walkthrough, and ends with `if __name__ == "__main__": main()`.
- Produces:
  - `print_queue`:
    - `simulate(documents: list[str], prints: int) -> tuple[list[str], list[str]]` enqueues all documents, then dequeues `prints` of them.
    - It returns `(printed, still_waiting)`, using `Queue`.
  - `browser_history`: `class Browser(home: str)` with `visit(url)`, `back() -> str`, `forward() -> str` and the `current: str` property.
    - It uses two `Stack`s.
    - Visiting clears the forward history.
    - `back` and `forward` with no history raise `IndexError`.
  - `rpn`: `evaluate(expression: str) -> float`.
    - Tokens are separated by whitespace. The operators are `+ - * / ^`.
    - It uses `Stack`.
    - It raises `ValueError` for a missing operand, a leftover operand, or an unknown token.
    - Division by zero raises `ZeroDivisionError`.
  - `expression`:
    - `operators(expression: str) -> list[str]` returns the operators `+ - * / ^` in order. This is the fixed version of original ex09, which wrongly counted parentheses as operators.
    - `is_balanced(expression: str) -> bool` handles `()[]{}` with a `Stack`.
  - `undo_redo`: `class TextEditor` with the `text: str` property, `write(s)`, `delete(n)`, `undo() -> None` and `redo() -> None`.
    - Each edit is pushed onto an undo `Stack`.
    - A new edit clears the redo stack.
    - Undo or redo with nothing to undo or redo is a no-op.
  - `palindrome`: `is_palindrome(text: str) -> bool`.
    - It ignores case, spaces, punctuation and accents, using `unicodedata.normalize("NFD")` and dropping the combining marks.
    - It compares a `Stack` pass (reversed) with a `Queue` pass (in order).
  - `hash_collisions`: `collisions(keys: list[int], size: int, hash_fn: Callable[[int], int]) -> dict[int, list[int]]`.
    - It returns only the buckets that hold more than one key.
    - It uses `HashMap(size, hash_fn=..., auto_resize=False)`.
  - `array_stats`, all using `dsa.sorting` or `HashMap`, none using `max`, `min` or `sorted`:
    - `largest_and_smallest(nums) -> tuple[int, int]`
    - `second_smallest(nums) -> int`
    - `third_largest(nums) -> int`
    - `median(nums) -> float`
    - `dedupe(nums) -> list[int]`, keeping order.
    - Values are distinct for the second and third rankings.
    - Each function raises `ValueError` when there are not enough distinct values, or when the input is empty.
  - `sleep_matrix`:
    - `SLEEP = Matrix([[8,6,7,8,6],[5,5,6,7,8],[6,7,8,6,5],[7,5,9,7,4]])`, with 4 weeks as rows and the days Monday to Friday as columns.
    - `DAYS = ["Segunda","Terça","Quarta","Quinta","Sexta"]`.
    - `best_day(m) -> tuple[str, float]` and `worst_day(m) -> tuple[str, float]`. The first one wins on ties.
    - `week_share(m) -> list[float]`, the percent of the month per week, rounded to 1 decimal.

**Steps:**

- [ ] **Step 1: Write the failing tests** (exact values):

```python
def test_print_queue():
    assert simulate(["relatorio.pdf", "contrato.docx", "foto.png"], 2) == (
        ["relatorio.pdf", "contrato.docx"], ["foto.png"])

def test_browser():
    b = Browser("home"); b.visit("a"); b.visit("b")
    assert b.back() == "a" and b.forward() == "b"
    b.back(); b.visit("c")
    with pytest.raises(IndexError):
        b.forward()

def test_rpn():
    assert evaluate("3 4 + 2 *") == 14
    assert evaluate("2 3 ^") == 8
    for bad in ("3 +", "1 2", "2 x 3", ""):   # Review Focus 5
        with pytest.raises(ValueError):
            evaluate(bad)

def test_expression():
    assert operators("(2+3)*(8-9)/(7^3)") == ["+", "*", "-", "/", "^"]
    assert is_balanced("{[()]}") and not is_balanced("(]") and not is_balanced("((")

def test_undo_redo():
    e = TextEditor(); e.write("Olá"); e.write(" mundo"); e.delete(6)
    e.undo(); assert e.text == "Olá mundo"
    e.undo(); assert e.text == "Olá"
    e.redo(); assert e.text == "Olá mundo"
    e.write("!"); e.redo(); assert e.text == "Olá mundo!"

def test_palindrome():
    assert is_palindrome("Socorram-me, subi no ônibus em Marrocos")
    assert is_palindrome("radar") and not is_palindrome("python")

def test_hash_collisions():
    assert collisions([2341, 4234, 2839, 430, 22, 397, 3920], 7, lambda x: x % 7) == {3: [2341, 430]}
    assert collisions([12, 44, 13, 88, 23, 94, 11, 39, 20, 16, 5], 11, lambda k: (2 * k + 5) % 11) == {
        4: [16, 5], 5: [44, 88, 11], 6: [94, 39], 7: [12, 23]}

def test_array_stats():
    xs = [3, 1, 4, 1, 5, 9, 2, 6]
    assert largest_and_smallest(xs) == (9, 1)
    assert second_smallest(xs) == 2 and third_largest(xs) == 5
    assert median(xs) == 3.5 and dedupe(xs) == [3, 1, 4, 5, 9, 2, 6]
    with pytest.raises(ValueError):
        third_largest([1, 1, 2])

def test_sleep_matrix():
    assert best_day(SLEEP) == ("Quarta", 30) and worst_day(SLEEP) == ("Terça", 23)
    assert week_share(SLEEP) == [26.9, 23.8, 24.6, 24.6]

@pytest.mark.parametrize("module", [...all nine...])
def test_main_runs(module, capsys):
    module.main(); assert capsys.readouterr().out.strip()
```

- [ ] **Step 2: Run.** Expected: it fails.
- [ ] **Step 3: Implement** the nine modules.
- [ ] **Step 4: Run** the full check. Also run `python -m examples.sleep_matrix`, which should print a pt-BR summary.
- [ ] **Step 5: Commit** with the message `feat: add examples from the original exercises`.

### Task 8: README

**Files:** Create `README.md`, in pt-BR.

The README has these sections, in order:

- **Header:**
  - Title: `# 🧱 Estruturas de dados em Python`.
  - A one-line pitch.
  - Badges: CI, Python 3.12+, mypy strict, and MIT license.
- **"O que tem aqui":** a table with structure, file and summary.
- **"Complexidade":** a Big-O table per operation.
  - `DynamicArray`: append is O(1) amortized, insert and remove are O(n), index is O(1).
  - `LinkedList`: append, appendleft, pop and popleft are O(1); remove and `in` are O(n).
  - `Stack`: push and pop are O(1) amortized.
  - `Queue`: enqueue is O(1) amortized and dequeue is O(1).
  - `HashMap`: get, set and delete are O(1) on average and O(n) in the worst case.
  - The five sorts, each with best, average and worst case, extra space, and whether it is stable.
  - `Matrix`: `@` is O(n·m·p).
- **"Decisões":**
  - Why a ring buffer: `list.pop(0)` is O(n).
  - Why 0.75 and doubling.
  - Why quick sort uses a random pivot plus a three-way partition, and loops on the larger side.
  - Why the structures are compared against the built-ins with Hypothesis.
- **"Exemplos":** each `python -m examples.<x>` command with one line of what it shows.
- **"Rodando":** venv, `pip install -e ".[dev]"`, `pytest`, `ruff check .`, `mypy`.
- **"Licença":** MIT.

Write no line that mentions the college or that these were coursework. Phrase it as "exercícios clássicos de estruturas de dados, reescritos com testes".

**Steps:**

- [ ] **Step 1: Write the README.** Make the test count match the `pytest -q` output.
- [ ] **Step 2: Run** the full check again. Then grep the whole repo for the college name and for "faculdade". Expected: 0 matches.
- [ ] **Step 3: Commit** with the message `docs: add README`.
