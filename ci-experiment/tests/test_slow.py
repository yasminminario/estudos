import time

from src.calculator import add


def test_slow_operation():
    time.sleep(3)
    assert add(1, 1) == 2
