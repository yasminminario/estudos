import pytest

from src.calculator import add, divide, multiply, power, subtract

ADD_CASES = [
    (0, 0, 0),
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
    (10, -5, 5),
    (100, 200, 300),
    (0.5, 0.5, 1.0),
    (-10, -10, -20),
]

SUBTRACT_CASES = [
    (10, 4, 6),
    (0, 0, 0),
    (5, 10, -5),
    (100, 50, 50),
    (-3, -3, 0),
    (7, 2, 5),
    (1.5, 0.5, 1.0),
    (-1, 1, -2),
]

MULTIPLY_CASES = [
    (0, 5, 0),
    (1, 1, 1),
    (3, 7, 21),
    (-2, 3, -6),
    (4, 4, 16),
    (10, 0.5, 5),
    (-1, -1, 1),
    (6, 7, 42),
]

DIVIDE_CASES = [
    (20, 4, 5),
    (9, 3, 3),
    (1, 2, 0.5),
    (-10, 2, -5),
    (7, 7, 1),
    (0, 5, 0),
    (15, 3, 5),
    (8, 2, 4),
]

POWER_CASES = [
    (2, 0, 1),
    (2, 1, 2),
    (2, 3, 8),
    (3, 2, 9),
    (5, 2, 25),
    (10, 1, 10),
    (4, 0.5, 2.0),
    (1, 100, 1),
]


@pytest.mark.parametrize("a,b,expected", ADD_CASES)
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", SUBTRACT_CASES)
def test_subtract_parametrized(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize("a,b,expected", MULTIPLY_CASES)
def test_multiply_parametrized(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a,b,expected", DIVIDE_CASES)
def test_divide_parametrized(a, b, expected):
    assert divide(a, b) == expected


@pytest.mark.parametrize("base,exponent,expected", POWER_CASES)
def test_power_parametrized(base, exponent, expected):
    assert power(base, exponent) == expected
