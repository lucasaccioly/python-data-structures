from types import ModuleType

import pytest

from examples import (
    array_stats,
    browser_history,
    expression,
    hash_collisions,
    palindrome,
    print_queue,
    rpn,
    sleep_matrix,
    undo_redo,
)
from examples.array_stats import dedupe, largest_and_smallest, median, second_smallest, third_largest
from examples.browser_history import Browser
from examples.expression import is_balanced, operators
from examples.hash_collisions import collisions
from examples.palindrome import is_palindrome
from examples.print_queue import simulate
from examples.rpn import evaluate
from examples.sleep_matrix import SLEEP, best_day, week_share, worst_day
from examples.undo_redo import TextEditor


def test_print_queue() -> None:
    assert simulate(["relatorio.pdf", "contrato.docx", "foto.png"], 2) == (
        ["relatorio.pdf", "contrato.docx"],
        ["foto.png"],
    )


def test_browser() -> None:
    b = Browser("home")
    b.visit("a")
    b.visit("b")
    assert b.back() == "a"
    assert b.forward() == "b"
    b.back()
    b.visit("c")
    assert b.current == "c"
    with pytest.raises(IndexError):
        b.forward()
    assert b.back() == "a"
    assert b.back() == "home"
    with pytest.raises(IndexError):
        b.back()


def test_rpn() -> None:
    assert evaluate("3 4 + 2 *") == 14
    assert evaluate("2 3 ^") == 8
    assert evaluate("10 4 - 2 /") == 3
    for bad in ("3 +", "1 2", "2 x 3", ""):  # Review Focus 5
        with pytest.raises(ValueError):
            evaluate(bad)
    with pytest.raises(ZeroDivisionError):
        evaluate("1 0 /")


def test_expression() -> None:
    assert operators("(2+3)*(8-9)/(7^3)") == ["+", "*", "-", "/", "^"]
    assert is_balanced("{[()]}")
    assert is_balanced("(2+3)*(8-9)/(7^3)")
    assert not is_balanced("(]")
    assert not is_balanced("((")
    assert not is_balanced("())")


def test_undo_redo() -> None:
    e = TextEditor()
    e.write("Olá")
    e.write(" mundo")
    e.delete(6)
    e.undo()
    assert e.text == "Olá mundo"
    e.undo()
    assert e.text == "Olá"
    e.redo()
    assert e.text == "Olá mundo"
    e.write("!")
    e.redo()
    assert e.text == "Olá mundo!"
    for _ in range(5):
        e.undo()
    assert e.text == ""


def test_palindrome() -> None:
    assert is_palindrome("Socorram-me, subi no ônibus em Marrocos")
    assert is_palindrome("radar")
    assert not is_palindrome("python")


def test_hash_collisions() -> None:
    assert collisions([2341, 4234, 2839, 430, 22, 397, 3920], 7, lambda x: x % 7) == {3: [2341, 430]}
    assert collisions([12, 44, 13, 88, 23, 94, 11, 39, 20, 16, 5], 11, lambda k: (2 * k + 5) % 11) == {
        4: [16, 5],
        5: [44, 88, 11],
        6: [94, 39],
        7: [12, 23],
    }


def test_array_stats() -> None:
    xs = [3, 1, 4, 1, 5, 9, 2, 6]
    assert largest_and_smallest(xs) == (9, 1)
    assert second_smallest(xs) == 2
    assert third_largest(xs) == 5
    assert median(xs) == 3.5
    assert median([5, 1, 3]) == 3
    assert dedupe(xs) == [3, 1, 4, 5, 9, 2, 6]
    with pytest.raises(ValueError):
        third_largest([1, 1, 2])
    with pytest.raises(ValueError):
        second_smallest([4, 4])
    for empty_fn in (median, largest_and_smallest):
        with pytest.raises(ValueError):
            empty_fn([])


def test_sleep_matrix() -> None:
    assert best_day(SLEEP) == ("Quarta", 30)
    assert worst_day(SLEEP) == ("Terça", 23)
    assert week_share(SLEEP) == [26.9, 23.8, 24.6, 24.6]


ALL_EXAMPLES = [
    print_queue,
    browser_history,
    rpn,
    expression,
    undo_redo,
    palindrome,
    hash_collisions,
    array_stats,
    sleep_matrix,
]


@pytest.mark.parametrize("module", ALL_EXAMPLES, ids=lambda m: m.__name__)
def test_main_runs(module: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    module.main()
    assert capsys.readouterr().out.strip()
