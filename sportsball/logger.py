"""Functions for creating a logger."""

import logging

from .args import parse_args
from .loglevel import LogLevel


def setup_logger() -> None:
    """Setup the logger to perform the required logging."""
    logging.basicConfig()
    logger = logging.getLogger()
    args = parse_args()
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
