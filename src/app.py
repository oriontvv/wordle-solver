from solver import Solver


def load_words(lang: str, length: int) -> set[str]:
    words = set()
    with open(f"words/{lang}.txt") as f:
        for line in f:
            word = line.strip().lower()
            if len(word) != length:
                continue
            words.add(word)
    return words


class App:
    def __init__(self, lang: str, length: int):
        self.lang = lang
        self.default_length = length
        words = load_words(lang, length)
        self.solver = Solver(self, words, length)

    def run(self):
        while not self.solver.is_done():
            self.print_guess(self.solver.get_next_guess())
            result = self.read_result()
            if result.strip() == 'reset':
                words = load_words(self.lang, self.default_length)
                self.solver.reset(words, self.default_length)
                continue
            try:
                self.solver.add_guess_result(result)
            except Exception as e:
                print(f"Error: {e}")

    def print_guess(self, word: str):
        print(f"Try '{word}'")

    def read_result(self) -> str:
        return input("> ").lower()
