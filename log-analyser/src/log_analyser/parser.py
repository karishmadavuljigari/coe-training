from datetime import datetime

from log_analyser.exceptions import InvalidLogLineError
from log_analyser.models import LogEntry


def parse_log_line(line: str) -> LogEntry:
    """Parse one log line into a LogEntry object."""
    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        raise InvalidLogLineError("Expected four parts in the log line")

    timestamp_text = f"{parts[0]} {parts[1]}"

    try:
        timestamp = datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise InvalidLogLineError("Invalid timestamp") from error

    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    level = parts[2]

    if level not in valid_levels:
        raise InvalidLogLineError("Invalid log level")

    message = parts[3]

    if not message.strip():
        raise InvalidLogLineError("Log message cannot be empty")

    return LogEntry(
        timestamp=timestamp,
        level=level,
        message=message,
    )
