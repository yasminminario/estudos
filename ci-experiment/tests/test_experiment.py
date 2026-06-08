from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_slow_test():
    assert VARIATION == "04-slow-test"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
