from __future__ import annotations
from collections import Counter
import copy
import re

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App


class Solver:
    def __init__(self, app: App, words: set(str), abc: str, start_word: str) -> None:
        self.app = app
        self.words = words
        self.possible_words = copy.deepcopy(words)
        self.abc = abc
        self.start_word = start_word
        self.step = 0
        self.variants = set()
        self.neg_variants = set()
        self.letters = [Letter(self) for _ in range(app.length)]

    def add_guess_result(self, guess: str):
        for ch, letter in zip(guess.strip().split(), self.letters):
            if ch == "*":
                continue
            if ch.endswith("?"):
                ch = ch[0]
                self.variants.add(ch)
                if ch in letter.unchecked:
                    letter.unchecked.remove(ch)
            elif ch.endswith("-"):
                ch = ch[0]
                self.neg_variants.add(ch)
            else:
                assert len(ch) == 1, "invalid format, expected 1 char"
                letter.found = ch

    def is_done(self) -> bool:
        return all(letter.is_done() for letter in self.letters)

    def get_next_guess(self) -> str:
        self.step += 1

        if self.step == 1:
            return self.start_word

        pattern = self._get_pattern()

        self.possible_words = set(
            word
            for word in self.possible_words
            if re.match(pattern, word)
            and all(variant in word for variant in self.variants)
            and not any(neg_variant in word for neg_variant in self.neg_variants)
        )

        freq = Counter()
        abc = set()
        for word in self.possible_words:
            for ch in word:
                abc.add(ch)
                freq[ch] += 1
        for letter in self.letters:
            letter.filter(abc)

        def max_freq(word):
            result = 0
            for ch in set(word):
                result += 3 * freq[ch]
            return -result

        print("possible variants:")
        words = list(self.possible_words)
        words.sort(key=max_freq)
        print("\n".join(words[:30]))
        print(f"Total: {len(self.possible_words)}")

        return words[0]

    def __str__(self) -> str:
        delim = "=" * 20
        result = f"""{delim}
{self.step}
variants: {self.variants}
"""
        for letter in self.letters:
            result += str(letter) + "\n"
        return result

    def _get_pattern(self) -> str:
        result = ""
        for letter in self.letters:
            if letter.found:
                result += letter.found
            else:
                result += "(" + "|".join(letter.unchecked) + ")"
        return result


class Letter:
    def __init__(self, solver: Solver):
        self.solver = solver
        self.unchecked = set(solver.abc)
        self.found: str | None = None

    def is_done(self) -> bool:
        return self.found is not None

    def filter(self, new_available: set[str]):
        if self.is_done():
            return
        self.unchecked = set(ch for ch in self.unchecked if ch in new_available)

    def __str__(self) -> str:
        if self.found:
            return f"\t found: {self.found}\n"
        return f"\t unchecked: {self.unchecked}\n"
