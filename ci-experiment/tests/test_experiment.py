from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_sequential():
    assert VARIATION == "07-sequential"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
