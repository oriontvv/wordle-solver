from __future__ import annotations

from solver import Solver
from words_loader import load_words


class CliApp:
    def __init__(self, lang: str, length: int):
        self.lang = lang
        self.default_length = length
        words = load_words(lang, length)
        self.solver = Solver(words, length)

    def run(self):
        while not self.solver.is_done():
            variants = self.solver.get_next_guess()
            self.print_variants(variants)

            result = self.read_user_input()
            if result == "new":
                words = load_words(self.lang, self.default_length)
                self.solver.reset(words)
                continue
            elif result == "exit":
                print("Good bye!")
                break

            try:
                self.solver.add_guess_result(result)
            except Exception as e:
                print(f"Error: {e}")

    def print_variants(self, variants: list[str]):
        if variants:
            print("Possible variants:")
            print("\n".join(variants))
            guess = variants[0]
            self.print_guess(guess)
        print(f"Total variants: {self.solver.total_variants()}")

    def print_guess(self, word: str | None):
        if word is None:
            print("I don't know such a word..")
        else:
            print(f"Try '{word}'")

    def read_user_input(self) -> str:
        return input("> ").lower().strip()
