from __future__ import annotations

import argparse
from pathlib import Path
import sys

from tabulate import tabulate

from .io import read_rows
from .reports import UnknownReportError, get_report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coffee consumption report")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="CSV files with student preparation data",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Report name (median-coffee)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    missing = [path for path in args.files if not Path(path).is_file()]
    if missing:
        print(f"File not found: {missing[0]}", file=sys.stderr)
        return 2

    try:
        report = get_report(args.report)
    except UnknownReportError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    rows = read_rows(args.files)
    report_rows = report.build(rows)

    print(tabulate(report_rows, headers=report.headers, tablefmt="github"))
    return 0
