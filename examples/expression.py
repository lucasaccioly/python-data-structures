"""Reading a math expression: list its operators and check that brackets are balanced with a stack."""

from dsa import Stack

OPERATORS = "+-*/^"
PAIRS = {")": "(", "]": "[", "}": "{"}


def operators(expression: str) -> list[str]:
    return [ch for ch in expression if ch in OPERATORS]


def is_balanced(expression: str) -> bool:
    """Every closing bracket must match the most recent unclosed opening one."""
    open_brackets = Stack[str]()
    for ch in expression:
        if ch in "([{":
            open_brackets.push(ch)
        elif ch in PAIRS and (not open_brackets or open_brackets.pop() != PAIRS[ch]):
            return False
    return not open_brackets


def main() -> None:
    expr = "(2+3)*(8-9)/(7^3)"
    print(f"Expressão: {expr}")
    print(f"Operadores: {' '.join(operators(expr))}")
    for e in [expr, "{[()]}", "(]", "(("]:
        print(f"{e!r} balanceada? {'sim' if is_balanced(e) else 'não'}")


if __name__ == "__main__":
    main()
