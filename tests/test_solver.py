import pytest
from src.solver import Solver


@pytest.fixture
def solver() -> Solver:
    words = ['aaaaa', 'aaaab', 'aaaac']
    return Solver(words=set(words), length=len(words[0]))


def test_simplest_solver(solver):
    solver.add_guess_result("a a a a a")
    variants = solver.get_next_guess()
    assert variants == ['aaaaa']


def test_solver(solver):
    solver.add_guess_result("a a a a b-")
    variants = solver.get_next_guess()
    assert set(variants) == set(('aaaaa', 'aaaac'))


def test_solver(solver):
    solver.add_guess_result("a a a b? c-")
    variants = solver.get_next_guess()
    assert variants == ['aaaab']


def test_too_long_guess(solver):
    with pytest.raises(Exception):
        solver.add_guess_result("a d- b? a e- a")


def test_too_short_guess(solver):
    with pytest.raises(Exception):
        solver.add_guess_result("a d- b? a")


def test_guess_without_spaces(solver):
    with pytest.raises(Exception):
        solver.add_guess_result("ad-b?a")
