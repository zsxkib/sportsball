"""The CLI for executing the data harvesting."""

import io
import logging
import sys
from contextlib import redirect_stdout

import pandas as pd

from . import __VERSION__
from .args import parse_args
from .data.league import league_from_str
from .logger import setup_logger
from .sportsball import SportsBall

_STDOUT_FILE = "-"


def main() -> None:
    """The main CLI function."""
    with redirect_stdout(sys.stderr):
        args = parse_args()
        setup_logger()

        logging.info("--- sportsball %s ---", __VERSION__)

        ball = SportsBall()
        league = ball.league(league_from_str(args.league), args.leaguemodel)
        
        try:
            df = league.to_frame()
        except Exception as e:
            logging.error("Error retrieving data: %s", str(e))
            # Create empty dataframe on error to ensure valid parquet output
            df = pd.DataFrame()
        
        # Ensure we have valid data for parquet output
        if df.empty:
            logging.warning("No data retrieved, creating minimal valid parquet file")
            # Create a minimal placeholder dataframe with expected columns for moneyball
            df = pd.DataFrame({
                "dt": [pd.Timestamp.now()],
                "no_data": [True], 
                "error": ["No games processed due to validation errors"]
            })
        
        handle = io.BytesIO()
        try:
            df.to_parquet(handle, compression="gzip")
            handle.seek(0)
            
            # Verify the parquet buffer is valid
            if handle.getbuffer().nbytes == 0:
                raise ValueError("Generated parquet buffer is empty")
        except Exception as e:
            logging.error("Error creating parquet file: %s, creating fallback", str(e))
            # Fallback: create a minimal valid parquet file with expected columns
            handle = io.BytesIO()
            pd.DataFrame({
                "dt": [pd.Timestamp.now()],
                "error": [True], 
                "message": [str(e)[:100]]
            }).to_parquet(handle, compression="gzip")
            handle.seek(0)
    if args.file == _STDOUT_FILE:
        try:
            sys.stdout.buffer.write(handle.getbuffer())
        except BrokenPipeError:
            # Handle broken pipe gracefully - downstream process closed pipe
            # This is normal behavior when piping to commands that don't need all data
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(1)
    else:
        with open(args.file, "wb") as fhandle:
            fhandle.write(handle.getbuffer())


if __name__ == "__main__":
    main()
