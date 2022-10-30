import pytest
from src.solver import Solver


@pytest.fixture
def solver() -> Solver:
    words = ["aaaaa", "aaaab", "aaaac"]
    return Solver(words=set(words), length=len(words[0]))


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
