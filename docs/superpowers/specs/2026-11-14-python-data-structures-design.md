# python-data-structures — design

Status: approved by Lucas on 2026-11-14.

## Intent

Portfolio project 5 for Lucas's job hunt. Lucas has five private college repos of beginner exercises (hash table, queue/stack, sequential list, sorting, matrix): 38 files with no tests, some bugs, and informal example data. Published as they are, they would weaken a portfolio that already has FinTrack and FlowBoard. The goal is one public repo that shows solid fundamentals to a recruiter: data structures written from scratch, clean, typed, tested, and explained.

## Goals

- A zero-dependency Python package `dsa` with these structures, each written from scratch and not wrapping the built-in equivalent:
  - `DynamicArray`: a sequential list that doubles its capacity when full. Origin: ListaSequencial.
  - `LinkedList`: a doubly linked list.
  - `Stack`: origin ListaFilaPilha.
  - `Queue`: a circular ring buffer with O(1) dequeue. Origin: ListaFilaPilha.
  - `HashMap`: separate chaining, resizing past a 0.75 load factor. Origin: TabelaHash.
  - `sorting`: selection, insertion, merge, quick and heap sort. Origin: Ordenação.
  - `Matrix`: add, transpose, multiply, row sums and column sums. Origin: Matriz.
- Pythonic behavior: `len()`, iteration, `in`, and `[]` where it makes sense.
- Tests:
  - pytest, plus Hypothesis property tests that check each structure against its built-in equivalent (`list`, `dict`, `collections.deque`, `sorted`).
  - ruff, and mypy `--strict`.
  - GitHub Actions CI on Python 3.12 and 3.14.
- `examples/`: the original exercises rewritten with the library, fixed, with neutral data. Each example has a test, so it can't silently break. The examples are:
  - print queue
  - browser back/forward
  - RPN calculator
  - undo/redo
  - palindrome
  - hash collisions
  - median and third-largest
  - sleep-hours matrix
- A pt-BR README with:
  - a Big-O table for every operation
  - the reasons behind each structure (why a ring buffer, why 0.75)
  - how to run it

## Non-goals

Benchmarks, trees, graphs, and publishing to PyPI.

## Anti-goals

- No name of the college or of any employer anywhere.
- No copying of the private repos' history: this is a fresh repo, and the private repos stay untouched.
- No silly or informal example data.

## Constraints

- Code, identifiers, docstrings and commits are in English. README and example output are in pt-BR, matching the other portfolio repos.
- The license is MIT, "© 2026 Lucas Accioly".
- Local Python is 3.14. `requires-python >=3.12`.

## Approaches

| Option | What it means | Outcome |
|---|---|---|
| Tested library | Rebuild from scratch, with the exercises as examples | **chosen**: it is the only option that shows fundamentals at the level of the other portfolio projects |
| Consolidate as-is | Move the 38 files into one repo, fix the bugs, add a README | rejected: still reads as coursework |

## Left to the builder

- Exact method names, error types (`IndexError`/`KeyError` like the built-ins), file layout under `src/dsa/`, and the example CLI shape.
