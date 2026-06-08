from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_parallel():
    assert VARIATION == "08-parallel"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
