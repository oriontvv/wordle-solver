from typing import Counter
from solver import Solver


class App:
    def __init__(self, lang: str, start_word: str):
        self.lang = lang
        self.length = len(start_word)
        words, abc = self._read_words()
        self.solver = Solver(self, words=words, abc=abc, start_word=start_word)

    def _read_words(self):
        words = set()
        abc = set()
        with open(f"words/{self.lang}.txt") as f:
            for line in f:
                word = line.strip().lower()
                if len(word) != self.length:
                    continue
                words.add(word)
                for letter in word:
                    abc.add(letter)

        return words, abc

    def run(self):
        while not self.solver.is_done():
            self.print_guess(self.solver.get_next_guess())
            result = self.read_result()
            self.solver.add_guess_result(result)
            print(self.solver)

    def print_guess(self, word: str):
        print(f"Try '{word}'")

    def read_result(self) -> str:
        return input("> ").lower()
