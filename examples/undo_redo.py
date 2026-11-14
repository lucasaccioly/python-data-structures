"""Text editor with undo/redo: every edit goes on a stack, and undoing moves it to a redo stack."""

from typing import Literal

from dsa import Stack

Edit = tuple[Literal["write", "delete"], str]


class TextEditor:
    def __init__(self) -> None:
        self._text = ""
        self._undo = Stack[Edit]()
        self._redo = Stack[Edit]()

    @property
    def text(self) -> str:
        return self._text

    def write(self, s: str) -> None:
        self._apply(("write", s))

    def delete(self, n: int) -> None:
        """Delete the last ``n`` characters (or all of them, if there are fewer)."""
        removed = self._text[len(self._text) - min(n, len(self._text)) :]
        self._apply(("delete", removed))

    def undo(self) -> None:
        if not self._undo:
            return
        kind, s = self._undo.pop()
        self._text = self._text[: len(self._text) - len(s)] if kind == "write" else self._text + s
        self._redo.push((kind, s))

    def redo(self) -> None:
        if not self._redo:
            return
        self._do(self._redo.pop())

    def _apply(self, edit: Edit) -> None:
        self._do(edit)
        self._redo = Stack[Edit]()  # a new edit starts a new timeline

    def _do(self, edit: Edit) -> None:
        kind, s = edit
        self._text = self._text + s if kind == "write" else self._text[: len(self._text) - len(s)]
        self._undo.push(edit)


def main() -> None:
    editor = TextEditor()
    editor.write("Olá")
    editor.write(" mundo")
    print(f"Texto: {editor.text!r}")
    editor.delete(6)
    print(f"Depois de apagar 6 caracteres: {editor.text!r}")
    editor.undo()
    print(f"Desfazer: {editor.text!r}")
    editor.undo()
    print(f"Desfazer: {editor.text!r}")
    editor.redo()
    print(f"Refazer: {editor.text!r}")


if __name__ == "__main__":
    main()
