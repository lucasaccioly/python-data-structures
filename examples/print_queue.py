"""Print queue: documents are printed in the order they arrive (FIFO)."""

from dsa import Queue


def simulate(documents: list[str], prints: int) -> tuple[list[str], list[str]]:
    """Queue every document, print ``prints`` of them; return (printed, still waiting)."""
    queue = Queue[str]()
    for doc in documents:
        queue.enqueue(doc)
    printed = [queue.dequeue() for _ in range(min(prints, len(queue)))]
    return printed, list(queue)


def main() -> None:
    queue = Queue[str]()
    for doc in ["relatorio.pdf", "contrato.docx", "foto.png"]:
        queue.enqueue(doc)
        print(f"Na fila: {doc}")
    print(f"Primeiro da fila: {queue.peek()} | último: {queue.peek_last()} | total: {len(queue)}")
    print(f"Imprimindo: {queue.dequeue()}")
    print(f"Ainda na fila: {list(queue)}")


if __name__ == "__main__":
    main()
