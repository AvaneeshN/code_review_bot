from dataclasses import dataclass


@dataclass
class ChangedFunction:
    file_path: str
    name: str
    start_line: int
    end_line: int

    def __post_init__(self) -> None:
        if self.start_line < 1:
            raise ValueError("start_line must be at least 1")

        if self.end_line < self.start_line:
            raise ValueError("end_line must not be before start_line")


@dataclass
class Finding:
    file_path: str
    line_number: int
    description: str
    evidence: str
    verified: bool = False

    def __post_init__(self) -> None:
        if self.line_number < 1:
            raise ValueError("line_number must be at least 1")
