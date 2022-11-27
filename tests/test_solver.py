import pytest
from app import load_words
from solver import Solver


@pytest.fixture
def solver() -> Solver:
    words = ["aaaaa", "aaaab", "aaaac"]
    return Solver(words=set(words), length=len(words[0]))


@pytest.fixture
def ru_solver() -> Solver:
    words = load_words(lang="ru", length=5)
    return Solver(words=set(words), length=5)


@pytest.mark.parametrize(
    "result,expected_variants",
    [
        ("a a a a a", ("aaaaa",)),
        ("a a a a b-", ("aaaaa", "aaaac")),
        ("a a a b? c-", ("aaaab",)),
    ],
)
def test_solver(result, expected_variants, solver):
    solver.add_guess_result(result)
    variants = solver.get_next_guess()
    assert set(variants) == set(expected_variants)


def test_too_long_guess(solver):
    with pytest.raises(Exception):
        solver.add_guess_result("a d- b? a e- a")


def test_too_short_guess(solver):
    with pytest.raises(Exception):
        solver.add_guess_result("a d- b? a")


def test_guess_without_spaces(solver):
    with pytest.raises(Exception):
        solver.add_guess_result("ad-b?a")


def test_real_guesses(ru_solver):
    assert ru_solver.get_next_guess()[0] == "кроат", ru_solver.get_next_guess()
    ru_solver.add_guess_result("к- р- о- а+ т")
    assert ru_solver.get_next_guess()[0] == "налет", ru_solver.get_next_guess()
    ru_solver.add_guess_result("н- а л е- т")
    assert ru_solver.get_next_guess()[0] == "сноха(*opt*)", ru_solver.get_next_guess()
    ru_solver.add_guess_result("с- н- о- х+ а+")
    assert ru_solver.get_next_guess()[0] == "халат", ru_solver.get_next_guess()
