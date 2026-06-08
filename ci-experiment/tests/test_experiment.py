from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_cache_on():
    assert VARIATION == "05-cache-on"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
