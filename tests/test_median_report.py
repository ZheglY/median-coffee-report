from coffee_report.io import read_rows
from coffee_report.reports import MedianCoffeeReport


def _write_csv(path, rows):
    header = "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
    body = "\n".join(rows) + "\n"
    path.write_text(header + body, encoding="utf-8")


def test_median_report_across_files(tmp_path):
    file_one = tmp_path / "part1.csv"
    file_two = tmp_path / "part2.csv"

    _write_csv(
        file_one,
        [
            "Alice,2024-06-01,100,7,6,ok,Math",
            "Bob,2024-06-01,300,6,7,ok,Math",
        ],
    )
    _write_csv(
        file_two,
        [
            "Alice,2024-06-02,200,7,6,ok,Math",
            "Bob,2024-06-02,100,6,7,ok,Math",
        ],
    )

    rows = read_rows([str(file_one), str(file_two)])
    report = MedianCoffeeReport()

    assert report.build(rows) == [["Bob", "200"], ["Alice", "150"]]
