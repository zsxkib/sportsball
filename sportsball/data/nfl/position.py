"""The enumeration of the different supported positions."""

from enum import StrEnum


class Position(StrEnum):
    """An enumeration over the different positions."""

    LINE_BACKER = "LB"
    DEFENSIVE_TACKLE = "DT"
    QUARTER_BACK = "QB"
    DEFENSIVE_LINESMAN = "DL"
    OFFENSIVE_LINESMAN = "OL"
    SAFETY = "S"
    WIDE_RECEIVER = "WR"
    GUARD = "G"
    RUNNING_BACK = "RB"
    TIGHT_END = "TE"
    OFFENSIVE_TACKLE = "OT"
