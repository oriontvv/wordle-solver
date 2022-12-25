from __future__ import annotations
import copy


class Letter:
    def __init__(self, index, abc: set[str]):
        self.index = index
        self.unchecked = copy.copy(abc)
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
            return f"(#{self.index}) found: {self.found}"
        return f"(#{self.index}) unchecked: {sorted(self.unchecked)}"
