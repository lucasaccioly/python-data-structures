"""Which keys collide in a fixed-size hash table with a given hash function."""

from collections.abc import Callable

from dsa import HashMap


def collisions(keys: list[int], size: int, hash_fn: Callable[[int], int]) -> dict[int, list[int]]:
    """Map each bucket that holds more than one key to its keys, in insertion order."""
    table = HashMap[int, None](size, hash_fn=hash_fn, auto_resize=False)
    for k in keys:
        table[k] = None
    return {i: bucket for i, bucket in enumerate(table.buckets()) if len(bucket) > 1}


def main() -> None:
    cases: list[tuple[str, list[int], int, Callable[[int], int]]] = [
        ("h(x) = x % 7", [2341, 4234, 2839, 430, 22, 397, 3920], 7, lambda x: x % 7),
        ("h(k) = (2k + 5) % 11", [12, 44, 13, 88, 23, 94, 11, 39, 20, 16, 5], 11, lambda k: (2 * k + 5) % 11),
    ]
    for name, keys, size, fn in cases:
        print(f"{name}, tabela de {size} posições, chaves {keys}")
        for index, bucket in collisions(keys, size, fn).items():
            print(f"  colisão na posição {index}: {bucket}")


if __name__ == "__main__":
    main()
