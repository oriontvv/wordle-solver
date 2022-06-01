from __future__ import annotations

import copy
import re
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App


class Solver:
    def __init__(self, app: App, words: set[str], lenght: int) -> None:
        self.app = app
        self.possible_words: set[str] = []
        self.step = 0
        self.variants = set()
        self.neg_variants = set()
        self.letters = []
        self.reset(words, lenght)

    def reset(self, words: set[str], lenght: int):
        if not words:
            raise Exception("Empty dictionary")
        self.step = 0
        self.variants = set()
        self.neg_variants = set()
        self.possible_words = words
        abc = {letter for word in words for letter in word}
        self.letters = [Letter(self, abc) for _ in range(lenght)]

    def add_guess_result(self, guess: str):
        chars = guess.strip().split()
        if len(chars) != len(self.letters):
            raise Exception("invalid format")

        for ch, letter in zip(chars, self.letters):
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
                if len(ch) != 1:
                    raise Exception("invalid format, expected 1 char")
                letter.found = ch

    def is_done(self) -> bool:
        return all(letter.is_done() for letter in self.letters)

    def get_next_guess(self) -> str:
        self.step += 1

        pattern = self._get_pattern()

        self.possible_words = set(
            word
            for word in self.possible_words
            if re.match(pattern, word)
            and all(variant in word for variant in self.variants)
            and not any(neg_variant in word for neg_variant in self.neg_variants)
        )
        abc = {letter for word in self.possible_words for letter in word}
        for letter in self.letters:
            letter.filter(abc)

        print("Possible variants:")
        variants = self.find_most_frequent_variants()
        print("\n".join(variants))
        print(f"Total: {len(self.possible_words)}")
        return variants[0]

    def find_most_frequent_variants(self, count: int = 30) -> list[str]:
        def max_freq(word):
            result = 0
            for ch in set(word):
                result += 3 * freq[ch]
            return -result

        freq = Counter()
        for word in self.possible_words:
            for ch in word:
                freq[ch] += 1

        words = list(self.possible_words)
        words.sort(key=max_freq)
        return words[:count]

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
    def __init__(self, solver: Solver, abc: str[str]):
        self.solver = solver
        self.unchecked = abc
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
