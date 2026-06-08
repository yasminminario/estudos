from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_final_collection():
    assert VARIATION == "10-final-collection"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
