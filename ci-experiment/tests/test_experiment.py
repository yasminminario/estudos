from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_failing_test():
    assert VARIATION == "02-failing-test"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
