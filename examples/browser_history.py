"""Browser back/forward buttons with two stacks."""

from dsa import Stack


class Browser:
    def __init__(self, home: str) -> None:
        self._current = home
        self._back = Stack[str]()
        self._forward = Stack[str]()

    @property
    def current(self) -> str:
        return self._current

    def visit(self, url: str) -> None:
        self._back.push(self._current)
        self._current = url
        self._forward = Stack[str]()  # a new page makes the old "forward" history unreachable

    def back(self) -> str:
        if not self._back:
            raise IndexError("não há página anterior")
        self._forward.push(self._current)
        self._current = self._back.pop()
        return self._current

    def forward(self) -> str:
        if not self._forward:
            raise IndexError("não há página seguinte")
        self._back.push(self._current)
        self._current = self._forward.pop()
        return self._current


def main() -> None:
    browser = Browser("inicio")
    for url in ["produtos", "carrinho", "pagamento"]:
        browser.visit(url)
        print(f"Visitou: {url}")
    print(f"Voltar → {browser.back()}")
    print(f"Voltar → {browser.back()}")
    print(f"Avançar → {browser.forward()}")
    browser.visit("ajuda")
    print("Visitou: ajuda (o histórico de 'avançar' foi descartado)")
    print(f"Página atual: {browser.current}")


if __name__ == "__main__":
    main()
