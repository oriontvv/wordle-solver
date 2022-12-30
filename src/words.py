from __future__ import annotations


def load_words(lang: str, length: int) -> set[str]:
    words = set()
    with open(f"words/{lang}.txt") as f:
        for line in f:
            word = line.strip()
            if len(word) != length:
                continue
            words.add(word.lower())
    return words
