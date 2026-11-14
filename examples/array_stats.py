"""Array questions answered with the package's own sorting and hash map (no max/min/sorted/set)."""

from dsa import HashMap
from dsa.sorting import merge_sort


def largest_and_smallest(nums: list[int]) -> tuple[int, int]:
    if not nums:
        raise ValueError("lista vazia")
    largest = smallest = nums[0]
    for n in nums[1:]:
        if n > largest:
            largest = n
        elif n < smallest:
            smallest = n
    return largest, smallest


def dedupe(nums: list[int]) -> list[int]:
    """Drop repeated values, keeping the first occurrence of each."""
    seen = HashMap[int, None]()
    result = []
    for n in nums:
        if n not in seen:
            seen[n] = None
            result.append(n)
    return result


def _nth_distinct(nums: list[int], n: int, *, largest: bool) -> int:
    distinct = merge_sort(dedupe(nums), reverse=largest)
    if len(distinct) < n:
        raise ValueError(f"são necessários pelo menos {n} valores distintos")
    return distinct[n - 1]


def second_smallest(nums: list[int]) -> int:
    return _nth_distinct(nums, 2, largest=False)


def third_largest(nums: list[int]) -> int:
    return _nth_distinct(nums, 3, largest=True)


def median(nums: list[int]) -> float:
    if not nums:
        raise ValueError("lista vazia")
    ordered = merge_sort(nums)
    mid = len(ordered) // 2
    return ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2


def main() -> None:
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    largest, smallest = largest_and_smallest(nums)
    print(f"Vetor: {nums}")
    print(f"Maior: {largest} | menor: {smallest}")
    print(f"Segundo menor: {second_smallest(nums)} | terceiro maior: {third_largest(nums)}")
    print(f"Mediana: {median(nums)}")
    print(f"Sem repetidos: {dedupe(nums)}")


if __name__ == "__main__":
    main()
