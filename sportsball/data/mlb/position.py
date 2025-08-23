"""The enumeration of the different supported positions."""

from enum import StrEnum


class Position(StrEnum):
    """An enumeration over the different positions."""

    LEFT_FIELD = "LF"
    RIGHT_FIELD = "RF"
    SECOND_BASEMAN = "2B"
    CATCHER = "C"
    SHORTSTOP = "SS"
    DESIGNATED_HITTER = "DH"
    FIRST_BASEMAN = "1B"
