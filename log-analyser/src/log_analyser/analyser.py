import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from log_analyser.exceptions import InvalidLogLineError
from log_analyser.models import AnalysisSummary, LogEntry
from log_analyser.parser import parse_log_line


def count_levels(entries: list[LogEntry]) -> Counter[str]:
    return Counter(entry.level for entry in entries)



def top_errors(entries: list[LogEntry], limit: int = 5) -> list[tuple[str, int]]:
    error_messages = [
        entry.message
        for entry in entries
        if entry.level in {"ERROR", "CRITICAL"}
    ]

    return Counter(error_messages).most_common(limit)




def get_time_range(
    entries: list[LogEntry],
) -> tuple[datetime | None, datetime | None]:
    if not entries:
        return None, None

    timestamps = [entry.timestamp for entry in entries]

    return min(timestamps), max(timestamps)



def analyse_entries(entries: list[LogEntry]) -> AnalysisSummary:
    level_counts = count_levels(entries)
    errors = top_errors(entries)
    start_time, end_time = get_time_range(entries)

    return AnalysisSummary(
        level_counts=level_counts,
        top_errors=errors,
        start_time=start_time,
        end_time=end_time,
        malformed_lines=0,
    )




def analyse_lines(lines: list[str]) -> AnalysisSummary:
    entries = []
    malformed_count = 0

    for line in lines:
        try:
            entry = parse_log_line(line)
            entries.append(entry)
        except InvalidLogLineError:
            malformed_count += 1

    summary = analyse_entries(entries)
    summary.malformed_lines = malformed_count

    return summary




def write_summary_json(
    summary: AnalysisSummary,
    output_path: Path,
) -> None:
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(summary.to_dict(), file, indent=4)
