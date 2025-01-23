"""The CLI for executing the data harvesting."""

import argparse
import io
import logging
import sys

from . import __VERSION__
from .data.league import League, league_from_str
from .loglevel import LogLevel
from .sportsball import SportsBall

_STDOUT_FILE = "-"


def main() -> None:
    """The main CLI function."""
    logging.basicConfig()
    logger = logging.getLogger()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--league",
        choices=list(League),
        help="The league to fetch data for.",
    )
    parser.add_argument(
        "--loglevel",
        default=LogLevel.INFO,
        choices=list(LogLevel),
        help="The loglevel to display logs at..",
        required=False,
    )
    parser.add_argument(
        "file",
        default=_STDOUT_FILE,
        help="The file to write the output to (- if to stdout).",
    )
    args = parser.parse_args()

    match args.loglevel:
        case LogLevel.DEBUG:
            logger.setLevel(logging.DEBUG)
        case LogLevel.INFO:
            logger.setLevel(logging.INFO)
        case LogLevel.WARN:
            logger.setLevel(logging.WARN)
        case LogLevel.ERROR:
            logger.setLevel(logging.ERROR)
        case _:
            raise ValueError(f"Unrecognised loglevel: {args.loglevel}")

    logging.info("--- sportsball %s ---", __VERSION__)

    ball = SportsBall()
    league = ball.league(league_from_str(args.league))
    df = league.to_frame()
    handle = io.BytesIO()
    df.to_parquet(handle, compression="gzip")
    handle.seek(0)
    if args.file == _STDOUT_FILE:
        sys.stdout.buffer.write(handle.getbuffer())
    else:
        with open(args.file, "wb") as fhandle:
            fhandle.write(handle.getbuffer())


if __name__ == "__main__":
    main()
