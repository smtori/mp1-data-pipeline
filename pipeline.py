"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from data_loaders import load_data
from pathlib import Path
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )


# Create a module-level logger
def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze a data file"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to a YAML configuration file" 
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    args = parser.parse_args()

    return args


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    p = Path(filepath)
    if not p.is_file():
        logger.error(f"Input file not found: '{filepath}'")
        return False

    logger.info(f"Input file validated: '{filepath}'")
    return True


def main():
    args = parse_arguments()
    setup_logging(verbose=args.verbose)

    logger = logging.getLogger(__name__)
    logger.debug(f"Arguments parsed: input={args.input}, config={args.config}, output={args.output}")

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # Load data
    try:
        data = load_data(Path(args.input))
        config = load_data(Path(args.config))
    except ValueError:
        sys.exit(1)

    # Save copy of original data
    df_original = data.copy()

    # Process the Data
    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    # Create cleaning report output
    cleaning_report = create_cleaning_report(df_original, data)
    print(cleaning_report)

    # Save cleaned dataframe as CSV
    data.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}.")

if __name__ == "__main__":
    main()
