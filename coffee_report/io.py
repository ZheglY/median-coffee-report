from __future__ import annotations

import csv
from typing import Iterable


def read_rows(paths: Iterable[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows.extend(reader)
    return rows
