from coffee_report.cli import main


def _write_csv(path):
    path.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,100,7,6,ok,Math\n",
        encoding="utf-8",
    )


def test_cli_unknown_report(tmp_path, capsys):
    csv_path = tmp_path / "data.csv"
    _write_csv(csv_path)

    code = main(["--files", str(csv_path), "--report", "nope"])

    captured = capsys.readouterr()
    assert code == 2
    assert "Unknown report" in captured.err


def test_cli_missing_file(tmp_path, capsys):
    missing = tmp_path / "missing.csv"

    code = main(["--files", str(missing), "--report", "median-coffee"])

    captured = capsys.readouterr()
    assert code == 2
    assert "File not found" in captured.err
