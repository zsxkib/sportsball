"""Functions for creating a logger."""

import logging

from .args import parse_args
from .loglevel import LogLevel


def setup_logger() -> None:
    """Setup the logger to perform the required logging."""
    logging.basicConfig(
        filename="sportsball.log",  # Specify the log file name
        filemode="w",  # 'a' for append, 'w' to overwrite
        encoding="utf-8",  # Optional, specify encoding
        level=logging.INFO,  # Set the logging level
        format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
        datefmt="%Y-%m-%d %H:%M:%S",  # Define the date and time format
    )
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
