from __future__ import annotations

import copy
import re
from collections import Counter

from letter import Letter


class Solver:
    def __init__(self, words: set[str], length: int) -> None:
        self.possible_words: set[str] = set()
        self.length = length
        self.letters: list[Letter] = []
        self.reset(words)
        self.found_chars: set[
            str
        ] = set()  # letters that must be in the word, not in their places

    def reset(self, words: set[str]):
        if not words:
            raise ValueError("Empty dictionary")
        self.original_words = words
        self.possible_words = copy.deepcopy(words)
        abc = {letter for word in words for letter in word}
        self.letters = [Letter(index, abc) for index in range(self.length)]
        self.found_chars = set()

    def add_guess_result(self, guess: str):
        chars = guess.strip().lower().split()
        if len(chars) != len(self.letters):
            raise ValueError(
                f"Invalid format: {chars}, expected {len(self.letters)} chars"
            )

        for ch, letter in zip(chars, self.letters):
            if ch.endswith(("?", "+")):
                ch = ch[0]
                self.found_chars.add(ch)
                letter.mark_checked(ch)
            elif ch.endswith("-"):
                ch = ch[0]
                for let in self.letters:
                    let.mark_checked(ch)
            else:
                if len(ch) != 1:
                    raise ValueError(f"Invalid format: {ch}, expected 1 char")
                letter.found = ch

    def is_done(self) -> bool:
        return all(letter.is_done() for letter in self.letters)

    def get_next_guess(self) -> list[str]:
        pattern = self.get_pattern()

        self.possible_words = {
            word
            for word in self.possible_words
            if re.match(pattern, word)
            and all(variant in word for variant in self.found_chars)
        }
        variants = self.find_most_frequent_variants()
        total_found = len([letter for letter in self.letters if letter.is_done()])
        if total_found >= 2 and len(self.possible_words) > 2:
            optimized_word = self.find_optimized_word(variants)
            if optimized_word not in variants:
                variants = [(optimized_word + "(*opt*)")] + variants

        return variants

    def total_variants(self) -> int:
        return len(self.possible_words)

    def find_most_frequent_variants(
        self, count: int = 30, additional_weight: set | None = None
    ) -> list[str]:
        _additional_weight = additional_weight or set()

        def max_freq(word):
            result = 0
            checked = set()
            for index, ch in enumerate(word):
                if ch in checked:
                    continue
                checked.add(ch)
                if ch in _additional_weight:
                    result += 100 * freqs[index][ch]  # make much more heavy
                else:
                    result += 3 * freqs[index][ch]
            return -result

        freqs: list[dict[str, int]] = [Counter() for _ in range(self.length)]
        for word in self.possible_words:
            for index, ch in enumerate(word):
                freqs[index][ch] += 1

        words = list(self.possible_words)
        words.sort(key=max_freq)
        return words[:count]

    def find_optimized_word(self, variants: list[str]) -> str:
        # try to find a word that covers as many as possible words
        solver = Solver(self.original_words, self.length)
        unchecked_letters = set()
        for variant in variants:
            for variant_letter, letter in zip(variant, self.letters):
                if letter.is_done():
                    continue
                unchecked_letters.add(variant_letter)

        optimized_variants = solver.find_most_frequent_variants(
            count=1, additional_weight=unchecked_letters
        )
        return optimized_variants[0]

    def __str__(self) -> str:
        result = f"found letters: {self.found_chars}\n"
        for letter in self.letters:
            result += str(letter) + "\n"
        return result

    def get_pattern(self) -> str:
        return "".join(letter.get_pattern() for letter in self.letters)
