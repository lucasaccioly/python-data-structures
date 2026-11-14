# 🧱 Estruturas de dados em Python

Estruturas de dados e algoritmos de ordenação clássicos escritos do zero, sem embrulhar o `list`/`dict` do Python, com tipagem estrita e testes que comparam cada estrutura com a equivalente nativa em milhares de casos gerados automaticamente.

[![CI](https://github.com/lucasaccioly/python-data-structures/actions/workflows/ci.yml/badge.svg)](https://github.com/lucasaccioly/python-data-structures/actions/workflows/ci.yml)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)
![mypy strict](https://img.shields.io/badge/mypy-strict-2a6db2)
![License MIT](https://img.shields.io/badge/license-MIT-blue)

## O que tem aqui

| Estrutura | Arquivo | Resumo |
|---|---|---|
| `DynamicArray` | [`dynamic_array.py`](src/dsa/dynamic_array.py) | Lista sequencial que dobra de capacidade quando enche |
| `LinkedList` | [`linked_list.py`](src/dsa/linked_list.py) | Lista duplamente encadeada |
| `Stack` | [`stack.py`](src/dsa/stack.py) | Pilha (LIFO), em cima do `DynamicArray` |
| `Queue` | [`queue.py`](src/dsa/queue.py) | Fila (FIFO) em buffer circular |
| `HashMap` | [`hash_map.py`](src/dsa/hash_map.py) | Tabela hash com encadeamento e redimensionamento |
| `sorting` | [`sorting.py`](src/dsa/sorting.py) | Selection, insertion, merge, quick e heap sort |
| `Matrix` | [`matrix.py`](src/dsa/matrix.py) | Soma, transposta, multiplicação, somas por linha e coluna |

As estruturas se comportam como as nativas: funcionam com `len()`, `for` e `in`, aceitam `[]` onde faz sentido (`DynamicArray`, `HashMap`, `Matrix`) e lançam os mesmos erros (`IndexError`, `KeyError`, `ValueError`).

```python
from dsa import HashMap, Queue
from dsa.sorting import quick_sort

fila = Queue[str]()
fila.enqueue("relatorio.pdf")
fila.enqueue("contrato.docx")
fila.dequeue()  # 'relatorio.pdf'

precos = HashMap[str, float]()
precos["café"] = 12.5
"café" in precos  # True

quick_sort([5, 2, 8, 1], reverse=True)  # [8, 5, 2, 1]
```

## Complexidade

| Estrutura | Operação | Custo |
|---|---|---|
| `DynamicArray` | `append` | O(1) amortizado |
| | `insert`, `pop(i)`, `remove` | O(n) |
| | `[i]`, `[i] = x`, `pop()` do fim | O(1) |
| | `in`, `index` | O(n) |
| `LinkedList` | `append`, `appendleft`, `pop`, `popleft` | O(1) |
| | `remove`, `in` | O(n) |
| `Stack` | `push` | O(1) amortizado |
| | `pop`, `peek` | O(1) |
| `Queue` | `enqueue` | O(1) amortizado |
| | `dequeue`, `peek`, `peek_last` | O(1) |
| `HashMap` | `get`, `set`, `delete`, `in` | O(1) em média, O(n) no pior caso |
| `Matrix` | `+`, `transpose`, `row_sums`, `col_sums` | O(n·m) |
| | `@` (n×m vezes m×p) | O(n·m·p) |

| Ordenação | Melhor | Médio | Pior | Espaço extra | Estável |
|---|---|---|---|---|---|
| `selection_sort` | O(n²) | O(n²) | O(n²) | O(1) | não |
| `insertion_sort` | O(n) | O(n²) | O(n²) | O(1) | sim |
| `merge_sort` | O(n log n) | O(n log n) | O(n log n) | O(n) | sim |
| `quick_sort` | O(n) | O(n log n) | O(n²)\* | O(log n) | não |
| `heap_sort` | O(n log n) | O(n log n) | O(n log n) | O(1) | não |

\* Com pivô aleatório, o pior caso depende de azar, não da entrada. O melhor caso O(n) é quando todos os valores são iguais, graças à partição em três partes.

Todas as funções de ordenação devolvem uma lista nova (a entrada não é alterada) e aceitam `reverse=True`. O espaço extra da tabela não conta essa cópia.

## Decisões

- **Fila em buffer circular.** Uma fila feita com `list.pop(0)` desloca todos os elementos a cada saída, então cada `dequeue` custa O(n). Aqui, o início da fila só anda uma posição e dá a volta no fim do bloco, então `dequeue` é O(1). Quando o bloco enche, ele dobra e os itens são copiados em ordem.
- **Tabela hash com 75% de ocupação.** Passou de 3/4 da capacidade, a tabela dobra e redistribui as chaves. Isso mantém as listas de cada posição curtas (busca O(1) em média). Como a capacidade dobra, o custo da redistribuição dividido pelas inserções é O(1).
- **Quick sort que não estoura a pilha.** Pivô aleatório (entrada já ordenada não vira O(n²)), partição em três partes, "menor / igual / maior" (muitos repetidos não degradam) e recursão só na parte menor, com um laço na maior, o que limita a profundidade a O(log n). Há um teste com 10 mil itens já ordenados, invertidos e todos iguais.
- **Estabilidade também no `reverse`.** Em `insertion_sort` e `merge_sort`, itens iguais mantêm a ordem original nos dois sentidos, como no `sorted` do Python.
- **Testes contra as nativas.** Cada estrutura com estado (`DynamicArray`, `LinkedList`, `Stack`, `Queue`, `HashMap`) roda numa máquina de estados do [Hypothesis](https://hypothesis.readthedocs.io/), que aplica sequências aleatórias de operações nela e na equivalente nativa (`list`, `deque`, `dict`) e confere que as duas sempre terminam iguais. A ordenação e a `Matrix` usam testes de propriedade contra `sorted` e `sum` com entradas geradas. Quando algo diverge, o Hypothesis reduz o caso ao menor exemplo que falha.

## Exemplos

Exercícios clássicos de estruturas de dados, reescritos usando o pacote e cobertos por testes:

| Comando | O que mostra |
|---|---|
| `python -m examples.print_queue` | Fila de impressão: primeiro a chegar, primeiro a imprimir |
| `python -m examples.browser_history` | Voltar/avançar do navegador com duas pilhas |
| `python -m examples.rpn` | Calculadora em notação polonesa reversa (`3 4 + 2 *` = 14) |
| `python -m examples.expression` | Operadores de uma expressão e parênteses balanceados |
| `python -m examples.undo_redo` | Desfazer/refazer de um editor de texto |
| `python -m examples.palindrome` | Palíndromo ignorando acentos e pontuação, com pilha e fila |
| `python -m examples.hash_collisions` | Colisões numa tabela hash de tamanho fixo |
| `python -m examples.array_stats` | Maior, menor, segundo menor, terceiro maior, mediana, sem repetidos |
| `python -m examples.sleep_matrix` | Matriz de horas de sono: melhor e pior dia, % por semana |

## Rodando

Requisito: Python 3.12 ou mais novo. O pacote não tem dependências; as de desenvolvimento são pytest, Hypothesis, ruff e mypy.

```bash
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -e ".[dev]"

pytest                           # 54 testes
ruff check . && ruff format --check .
mypy                             # modo estrito
```

O CI roda tudo isso no Python 3.12 e 3.14 a cada push.

## Licença

[MIT](LICENSE) © Lucas Accioly
