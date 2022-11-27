from __future__ import annotations


class Letter:
    def __init__(self, abc: set[str]):
        self.unchecked = abc
        self.found: str | None = None

    def is_done(self) -> bool:
        return self.found is not None

    def mark_checked(self, checked_char: str):
        self.unchecked.discard(checked_char)

    def get_pattern(self) -> str:
        if self.found:
            return self.found
        return "(" + "|".join(self.unchecked) + ")"

    def __str__(self) -> str:
        if self.found:
            return f"\t found: {self.found}\n"
        return f"\t unchecked: {self.unchecked}\n"
