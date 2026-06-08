import pytest

from src.calculator import add, divide, multiply, power, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(3, 7) == 21


def test_divide():
    assert divide(20, 4) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="division by zero"):
        divide(1, 0)


def test_power():
    assert power(2, 3) == 8
