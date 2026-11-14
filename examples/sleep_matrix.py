"""Hours of sleep over a month: 4 weeks (rows) × 5 weekdays (columns)."""

from dsa import Matrix

SLEEP = Matrix(
    [
        [8, 6, 7, 8, 6],
        [5, 5, 6, 7, 8],
        [6, 7, 8, 6, 5],
        [7, 5, 9, 7, 4],
    ]
)
DAYS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]


def _pick_day(m: Matrix, *, best: bool) -> tuple[str, float]:
    totals = m.col_sums()
    chosen = 0
    for i, total in enumerate(totals):
        if (total > totals[chosen]) if best else (total < totals[chosen]):  # first one wins ties
            chosen = i
    return DAYS[chosen], totals[chosen]


def best_day(m: Matrix) -> tuple[str, float]:
    return _pick_day(m, best=True)


def worst_day(m: Matrix) -> tuple[str, float]:
    return _pick_day(m, best=False)


def week_share(m: Matrix) -> list[float]:
    """Percent of the month's sleep in each week, rounded to one decimal."""
    weeks = m.row_sums()
    month = sum(weeks)
    return [round(w / month * 100, 1) for w in weeks]


def main() -> None:
    day, hours = best_day(SLEEP)
    print(f"Dia com mais descanso: {day} ({hours:g} h no mês)")
    day, hours = worst_day(SLEEP)
    print(f"Dia com menos descanso: {day} ({hours:g} h no mês)")
    for week, (total, share) in enumerate(zip(SLEEP.row_sums(), week_share(SLEEP), strict=True), start=1):
        print(f"Semana {week}: {total:g} h ({share}% do mês)")


if __name__ == "__main__":
    main()
