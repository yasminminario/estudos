from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_more_tests():
    assert VARIATION == "03-more-tests"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
