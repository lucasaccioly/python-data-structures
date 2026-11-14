"""Palindrome check: a stack gives the letters backwards, a queue gives them in order."""

import unicodedata

from dsa import Queue, Stack


def _letters(text: str) -> list[str]:
    """Lowercase letters and digits only, with accents removed (ô → o)."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return [ch for ch in decomposed if ch.isalnum() and not unicodedata.combining(ch)]


def is_palindrome(text: str) -> bool:
    stack, queue = Stack[str](), Queue[str]()
    for ch in _letters(text):
        stack.push(ch)
        queue.enqueue(ch)
    return all(stack.pop() == queue.dequeue() for _ in range(len(stack)))


def main() -> None:
    for text in ["radar", "Socorram-me, subi no ônibus em Marrocos", "estrutura"]:
        print(f"{text!r} é palíndromo? {'sim' if is_palindrome(text) else 'não'}")


if __name__ == "__main__":
    main()
