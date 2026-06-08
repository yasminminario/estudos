from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_baseline():
    assert VARIATION == "01-baseline-passing"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
