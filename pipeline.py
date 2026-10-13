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
from pathlib import Path
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)
logger = logging.getLogger(__name__)


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

    # Read validation from the config
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    # Save copy of original data
    df_original = data.copy()

    # Validate the data
    rows_before = len(data)

    logger.info(f"Rows before validation: {rows_before}")
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Rows after validation: {len(data)}")

    # Process the Data
    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    # Create cleaning report output
    cleaning_report = create_cleaning_report(df_original, data)
    print(cleaning_report)

    # Save cleaned dataframe as CSV
    output_path = save_data(data, args.output)
    logger.info(f"Saved cleaned data to {output_path}.")


if __name__ == "__main__":
    main()
