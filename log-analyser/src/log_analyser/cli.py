
import logging
from pathlib import Path

from log_analyser.analyser import analyse_lines, write_summary_json

PROJECT_DIR = Path(__file__).resolve().parents[2]

DEFAULT_INPUT = PROJECT_DIR / "data" / "sample.log"
DEFAULT_OUTPUT = PROJECT_DIR / "output" / "summary.json"


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        with DEFAULT_INPUT.open(encoding="utf-8") as file:
            lines = file.readlines()

        summary = analyse_lines(lines)

        DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        write_summary_json(summary, DEFAULT_OUTPUT)

        logging.info("Analysis completed successfully.")
        logging.info("Malformed lines found: %d", summary.malformed_lines)
        logging.info("JSON summary saved to %s", DEFAULT_OUTPUT)

    except OSError:
        logging.exception(
            "Could not read the input file or write the output file."
        )


if __name__ == "__main__":
    main()
