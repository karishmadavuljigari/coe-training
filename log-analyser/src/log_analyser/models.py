from collections import Counter
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str




@dataclass
class AnalysisSummary:
    level_counts: Counter[str]
    top_errors: list[tuple[str, int]]
    start_time: datetime | None
    end_time: datetime | None
    malformed_lines: int

    
    def to_dict(self) -> dict:
        return {
            "level_counts": dict(self.level_counts),
            "top_errors": [
                {"message": message, "count": count}
                for message, count in self.top_errors
            ],
            "start_time": (
                self.start_time.isoformat() if self.start_time else None
            ),
            "end_time": (
                self.end_time.isoformat() if self.end_time else None
            ),
            "malformed_lines": self.malformed_lines,
        }

