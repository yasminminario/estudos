from src.experiment import DESCRIPTION, VARIATION


def test_variation_is_cache_off():
    assert VARIATION == "06-cache-off"


def test_variation_has_description():
    assert len(DESCRIPTION) > 0
