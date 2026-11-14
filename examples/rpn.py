"""Reverse Polish Notation calculator: operands go on a stack, each operator pops two."""

from collections.abc import Callable

from dsa import Stack

OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "^": lambda a, b: a**b,
}


def evaluate(expression: str) -> float:
    """Evaluate e.g. ``"3 4 + 2 *"`` (= 14). Raises ValueError for malformed input."""
    stack = Stack[float]()
    for token in expression.split():
        if token in OPERATIONS:
            if len(stack) < 2:
                raise ValueError(f"faltam operandos para '{token}'")
            b, a = stack.pop(), stack.pop()
            stack.push(OPERATIONS[token](a, b))
        else:
            try:
                stack.push(float(token))
            except ValueError:
                raise ValueError(f"token desconhecido: '{token}'") from None
    if len(stack) != 1:
        raise ValueError("a expressão deve resultar em exatamente um valor")
    return stack.pop()


def main() -> None:
    for expr in ["3 4 + 2 *", "5 1 2 + 4 * + 3 -", "2 3 ^", "3 +"]:
        try:
            print(f"{expr} = {evaluate(expr):g}")
        except ValueError as e:
            print(f"{expr} → erro: {e}")


if __name__ == "__main__":
    main()
