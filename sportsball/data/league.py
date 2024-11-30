"""The enumeration of the different supported leagues."""

from enum import StrEnum


class League(StrEnum):
    """An enumeration over the different leagues."""

    AFL = "afl"
    NFL = "nfl"
    NBA = "nba"
