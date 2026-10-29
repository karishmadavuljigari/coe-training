
from datetime import datetime

import pytest
from log_analyser.exceptions import InvalidLogLineError
from log_analyser.parser import parse_log_line


def test_parse_valid_log_line():
    line = "2026-10-29 09:01:00 ERROR Database connection failed"

    entry = parse_log_line(line)

    assert entry.timestamp == datetime(2026, 10, 29, 9, 1, 0)
    assert entry.level == "ERROR"
    assert entry.message == "Database connection failed"


def test_parse_invalid_timestamp():
    line = "2026-15-45 09:01:00 ERROR Database connection failed"

    with pytest.raises(InvalidLogLineError):
        parse_log_line(line)


def test_parse_invalid_log_level():
    line = "2026-10-29 09:01:00 EROR Database connection failed"

    with pytest.raises(InvalidLogLineError):
        parse_log_line(line)



def test_parse_empty_message():
    line = "2026-10-29 09:01:00 ERROR "

    with pytest.raises(InvalidLogLineError):
        parse_log_line(line)



def test_parse_incomplete_log_line():
    line = "2026-10-29 ERROR"

    with pytest.raises(InvalidLogLineError):
        parse_log_line(line)



def test_parse_info_log_line():
    line = "2026-10-29 10:30:00 INFO Application started"

    entry = parse_log_line(line)

    assert entry.level == "INFO"
    assert entry.message == "Application started"



def test_parse_critical_log_line():
    line = "2026-10-29 11:45:00 CRITICAL Server unavailable"

    entry = parse_log_line(line)

    assert entry.level == "CRITICAL"
    assert entry.message == "Server unavailable"



def test_parse_message_with_multiple_words():
    line = "2026-10-29 12:00:00 WARNING Disk space is running low"

    entry = parse_log_line(line)

    assert entry.level == "WARNING"
    assert entry.message == "Disk space is running low"
