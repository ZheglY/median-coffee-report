from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Iterable


class UnknownReportError(ValueError):
    pass


def format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return format(value, "g")


@dataclass(frozen=True)
class Report:
    name: str
    headers: tuple[str, str]

    def build(self, rows: Iterable[dict[str, str]]) -> list[list[str]]:
        raise NotImplementedError


class MedianCoffeeReport(Report):
    def __init__(self) -> None:
        super().__init__(name="median-coffee", headers=("student", "median_coffee_spent"))

    def build(self, rows: Iterable[dict[str, str]]) -> list[list[str]]:
        per_student: dict[str, list[float]] = {}
        for row in rows:
            student = row["student"].strip()
            coffee_spent = float(row["coffee_spent"])
            per_student.setdefault(student, []).append(coffee_spent)

        medians: list[tuple[str, float]] = [
            (student, median(values)) for student, values in per_student.items()
        ]
        medians.sort(key=lambda item: (-item[1], item[0]))

        return [[student, format_number(value)] for student, value in medians]


REPORTS: dict[str, Report] = {
    "median-coffee": MedianCoffeeReport(),
}


def get_report(name: str) -> Report:
    try:
        return REPORTS[name]
    except KeyError as exc:
        raise UnknownReportError(f"Unknown report: {name}") from exc
