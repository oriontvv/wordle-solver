import pytest
from words_loader import load_words
from solver import Solver


@pytest.fixture
def solver() -> Solver:
    words = ["aaaaa", "aaaab", "aaaac"]
    return Solver(words=set(words), length=5)


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
    with pytest.raises(ValueError):
        solver.add_guess_result("a d- b? a e- a")


def test_too_short_guess(solver):
    with pytest.raises(ValueError):
        solver.add_guess_result("a d- b? a")


def test_guess_without_spaces(solver):
    with pytest.raises(ValueError):
        solver.add_guess_result("ad-b?a")


def test_guess_extra_letter(solver):
    with pytest.raises(ValueError):
        solver.add_guess_result("a d- b? auf e-")


def test_real_guesses(ru_solver):
    guess = ru_solver.get_next_guess()
    assert guess and guess[0] == "кроат", guess

    ru_solver.add_guess_result("к- р- о- а+ т")
    guess = ru_solver.get_next_guess()
    assert guess and guess[0] == "налет", guess

    ru_solver.add_guess_result("н- а л е- т")
    guess = ru_solver.get_next_guess()
    assert guess and guess[0] == "салют", guess

    ru_solver.add_guess_result("с- н- о- х+ а+")
    guess = ru_solver.get_next_guess()
    assert not guess


def test_real_guesses_1(ru_solver):
    assert ru_solver.get_next_guess()[0] == "кроат", ru_solver.get_next_guess()
    ru_solver.add_guess_result("к- р+ о а- т+")
    guess = ru_solver.get_next_guess()
    assert "шторм" in guess, guess
    assert "фронт" not in guess, guess


def test_opt_guess(ru_solver):
    guess = ru_solver.get_next_guess()
    assert guess and guess[0] == "кроат", guess

    ru_solver.add_guess_result("к+ р+ о+ а+ т-")
    ru_solver.add_guess_result("п- о р к а")
    guess = ru_solver.get_next_guess()
    assert guess and guess[0] == "гранд(*opt*)", guess


def test_solver_display(solver):
    assert (
        str(solver)
        == """found letters: set()
(#0) unchecked: ['a', 'b', 'c']
(#1) unchecked: ['a', 'b', 'c']
(#2) unchecked: ['a', 'b', 'c']
(#3) unchecked: ['a', 'b', 'c']
(#4) unchecked: ['a', 'b', 'c']
"""
    ), str(solver)

    solver.add_guess_result("a a a a b")

    assert (
        str(solver)
        == """found letters: set()
(#0) found: a
(#1) found: a
(#2) found: a
(#3) found: a
(#4) found: b
"""
    ), str(solver)
    assert solver.is_done()


def test_error_when_empty_dict():
    with pytest.raises(ValueError):
        Solver(words=set(), length=5)


def test_solver_methods(solver: Solver):
    assert not solver.is_done()
    assert solver.total_variants() == 3
