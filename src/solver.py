from __future__ import annotations

import copy
import re
from collections import Counter


class Solver:
    def __init__(self, words: set[str], lenght: int) -> None:
        self.possible_words: set[str] = set()
        self.lenght = lenght
        self.step = 0
        self.variants: set[str] = set()
        self.neg_variants: set[str] = set()
        self.letters: list[Letter] = []
        self.reset(words)

    def reset(self, words: set[str]):
        if not words:
            raise Exception("Empty dictionary")
        self.step = 0
        self.variants = set()
        self.neg_variants = set()
        self.original_words = words
        self.possible_words = copy.deepcopy(words)
        abc = {letter for word in words for letter in word}
        self.letters = [Letter(self, abc) for _ in range(self.lenght)]

    def add_guess_result(self, guess: str):
        chars = guess.strip().split()
        if len(chars) != len(self.letters):
            raise Exception(
                f"Invalid format: {chars}, expected {len(self.letters)} chars"
            )

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
                    raise Exception(f"Invalid format: {ch}, expected 1 char")
                letter.found = ch

    def is_done(self) -> bool:
        return all(letter.is_done() for letter in self.letters)

    def get_next_guess(self) -> list[str]:
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

        variants = self.find_most_frequent_variants()
        total_found = len([letter for letter in self.letters if letter.is_done()])
        if total_found >= 3 and len(self.possible_words) > 2:
            variants = self.find_optimized_word(variants) + variants

        return variants

    def total_variants(self) -> int:
        return len(self.possible_words)

    def find_most_frequent_variants(
        self, count: int = 30, additional_weight: set = None
    ) -> list[str]:
        additional_weight = additional_weight or set()

        def max_freq(word):
            result = 0
            for ch in set(word):
                if ch in additional_weight:
                    result += 100 * freq[ch]
                else:
                    result += 3 * freq[ch]
            return -result

        freq: dict[str, int] = Counter()
        for word in self.possible_words:
            for ch in word:
                freq[ch] += 1

        words = list(self.possible_words)
        words.sort(key=max_freq)
        return words[:count]

    def find_optimized_word(self, variants) -> list[str]:
        solver = Solver(self.original_words, self.lenght)
        unchecked_letters = set()
        for variant in variants:
            for variant_letter, letter in zip(variant, self.letters):
                if letter.is_done():
                    continue
                unchecked_letters.add(variant_letter)

        optimized_variants = solver.find_most_frequent_variants(
            count=1, additional_weight=unchecked_letters
        )
        return optimized_variants

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
    def __init__(self, solver: Solver, abc: set[str]):
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
