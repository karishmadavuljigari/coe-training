# Log Analyser

## Overview

The Log Analyser is a Python project that reads application log files, analyses log entries, and saves a summary as a JSON file.

## Features

- Parses log entries containing a timestamp, log level, and message.
- Counts log entries by level: DEBUG, INFO, WARNING, ERROR, and CRITICAL.
- Identifies the most frequent ERROR and CRITICAL messages.
- Finds the earliest and latest timestamps.
- Counts malformed lines without stopping the analysis.
- Saves the analysis summary as a JSON file.
- Uses logging to report the analysis status and errors.

## Project Structure

```text
log-analyser/
├── data/
│   └── sample.log
├── output/
│   └── summary.json
├── src/
│   └── log_analyser/
│       ├── __init__.py
│       ├── analyser.py
│       ├── cli.py
│       ├── exceptions.py
│       ├── models.py
│       └── parser.py
├── tests/
│   ├── test_analyser.py
│   └── test_parser.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Requirements

- Python
- pytest
- Ruff
- Pyright

Run the commands below from the repository root, where the `log-analyser` directory is located.

## Run the Project

```bash
PYTHONPATH=log-analyser/src python -m log_analyser.cli
```

The program reads `data/sample.log` and writes the analysis summary to `output/summary.json`.

## Run Tests

```bash
PYTHONPATH=log-analyser/src python -m pytest log-analyser/tests -v
```

## Code Quality

Run Ruff:

```bash
ruff check --config log-analyser/pyproject.toml log-analyser/src/log_analyser log-analyser/tests
```

Run Pyright:

```bash
PYTHONPATH=log-analyser/src pyright log-analyser/src/log_analyser log-analyser/tests
```

## Expected Results

The sample log contains eight valid entries. The analyser should report:

- 3 INFO entries
- 1 WARNING entry
- 2 ERROR entries
- 1 CRITICAL entry
- 1 DEBUG entry
- 0 malformed lines

The JSON summary includes the log-level counts, top errors, time range, and malformed-line count.