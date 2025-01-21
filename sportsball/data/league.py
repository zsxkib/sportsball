"""The enumeration of the different supported leagues."""

from enum import StrEnum


class League(StrEnum):
    """An enumeration over the different leagues."""

    AFL = "afl"
    NBA = "nba"
    NCAAB = "ncaab"
    NCAAF = "ncaaf"
    NFL = "nfl"


def long_name(league: League) -> str:
    """Find the leagues long name."""
    match league:
        case League.AFL:
            return "Australia Football League"
        case League.NBA:
            return "National Basketball League"
        case League.NCAAB:
            return "NCAA Division I Basketball"
        case League.NCAAF:
            return "NCAA Division I Football"
        case League.NFL:
            return "National Football League"
