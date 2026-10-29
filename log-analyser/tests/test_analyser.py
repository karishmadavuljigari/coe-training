import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from log_analyser.analyser import (
    analyse_entries,
    analyse_lines,
    count_levels,
    get_time_range,
    top_errors,
    write_summary_json,
)
from log_analyser.models import AnalysisSummary, LogEntry


def test_count_levels():
    entries = [
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 0, 0),
            level="INFO",
            message="Application started",
        ),
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 1, 0),
            level="ERROR",
            message="Database connection failed",
        ),
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 2, 0),
            level="INFO",
            message="Retry attempt started",
        ),
    ]

    result = count_levels(entries)

    assert result["INFO"] == 2
    assert result["ERROR"] == 1


def test_top_errors():
    entries = [
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 0, 0),
            level="ERROR",
            message="Database connection failed",
        ),
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 1, 0),
            level="ERROR",
            message="Database connection failed",
        ),
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 2, 0),
            level="CRITICAL",
            message="Server unavailable",
        ),
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 3, 0),
            level="INFO",
            message="Application started",
        ),
    ]

    result = top_errors(entries)

    assert result == [
        ("Database connection failed", 2),
        ("Server unavailable", 1),
    ]


def test_get_time_range():
    entries = [
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 5, 0),
            level="INFO",
            message="Later event",
        ),
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 0, 0),
            level="INFO",
            message="Earlier event",
        ),
    ]

    start_time, end_time = get_time_range(entries)

    assert start_time == datetime(2026, 10, 29, 9, 0, 0)
    assert end_time == datetime(2026, 10, 29, 9, 5, 0)


def test_analyse_entries():
    entries = [
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 0, 0),
            level="INFO",
            message="Application started",
        ),
        LogEntry(
            timestamp=datetime(2026, 10, 29, 9, 1, 0),
            level="ERROR",
            message="Database connection failed",
        ),
    ]

    summary = analyse_entries(entries)

    assert summary.level_counts["INFO"] == 1
    assert summary.level_counts["ERROR"] == 1
    assert summary.top_errors == [("Database connection failed", 1)]
    assert summary.start_time == datetime(2026, 10, 29, 9, 0, 0)
    assert summary.end_time == datetime(2026, 10, 29, 9, 1, 0)
    assert summary.malformed_lines == 0


def test_get_time_range_empty_entries():
    start_time, end_time = get_time_range([])

    assert start_time is None
    assert end_time is None


def test_analyse_lines_counts_malformed_lines():
    lines = [
        "2026-10-29 09:00:00 INFO Application started",
        "This is not a valid log line",
        "2026-10-29 09:02:00 ERROR Database connection failed",
        "2026-10-29 09:03:00 INVALID Something happened",
    ]

    summary = analyse_lines(lines)

    assert summary.level_counts["INFO"] == 1
    assert summary.level_counts["ERROR"] == 1
    assert summary.malformed_lines == 2


def test_analyse_sample_log_file():
    log_path = Path("log-analyser/data/sample.log")

    with log_path.open(encoding="utf-8") as file:
        lines = file.readlines()

    summary = analyse_lines(lines)

    assert sum(summary.level_counts.values()) == 8
    assert summary.level_counts["INFO"] == 3
    assert summary.level_counts["ERROR"] == 2
    assert summary.malformed_lines == 0


def test_summary_to_dict():
    summary = AnalysisSummary(
        level_counts=Counter({"INFO": 2, "ERROR": 1}),
        top_errors=[("Database connection failed", 1)],
        start_time=datetime(2026, 10, 29, 9, 0, 0),
        end_time=datetime(2026, 10, 29, 9, 2, 0),
        malformed_lines=1,
    )

    result = summary.to_dict()

    assert result["level_counts"] == {"INFO": 2, "ERROR": 1}
    assert result["top_errors"] == [
        {"message": "Database connection failed", "count": 1}
    ]
    assert result["start_time"] == "2026-10-29T09:00:00"
    assert result["end_time"] == "2026-10-29T09:02:00"
    assert result["malformed_lines"] == 1


def test_write_summary_json(tmp_path):
    summary = AnalysisSummary(
        level_counts=Counter({"INFO": 1}),
        top_errors=[("Database connection failed", 1)],
        start_time=datetime(2026, 10, 29, 9, 0, 0),
        end_time=datetime(2026, 10, 29, 9, 0, 0),
        malformed_lines=0,
    )

    output_path = tmp_path / "summary.json"

    write_summary_json(summary, output_path)

    assert output_path.exists()

    result = json.loads(output_path.read_text(encoding="utf-8"))

    assert result["level_counts"] == {"INFO": 1}
    assert result["top_errors"] == [
        {"message": "Database connection failed", "count": 1}
    ]
    assert result["malformed_lines"] == 0
