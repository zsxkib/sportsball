"""AFL aussportsbetting bookie model."""

from ...bookie_model import BookieModel


def create_afl_aussportsbetting_bookie_model() -> BookieModel:
    """Create bookie model from aus sports betting."""
    return BookieModel(identifier="bet365", name="Bet365")
