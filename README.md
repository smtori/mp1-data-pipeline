This pipeline is a command-line tool that takes a raw CSV file and a YAML configuration file and produces a cleaned CSV along with a cleaning report. pipeline.py coordinates the workflow: it parses the --input, --config, --output, and --verbose arguments, sets up logging, and calls each stage in order, exiting with status code 1 if any stage fails. Data first passes through src/utils.py, which configures logging and confirms the input files exist, and src/data_loaders.py, which loads the CSV into a DataFrame and the YAML into a configuration dictionary. Next, src/data_validator.py checks that every required column is present, removes rows whose numeric columns contain non-numeric values, and converts those columns to a numeric type. The validated DataFrame then goes to the processing module, which removes duplicate rows, drops rows with missing values, and filters outliers using the IQR method, all controlled by the configuration file rather than hard-coded values. Finally, the report module compares the original and cleaned data to summarize what was removed, and src/data_output.py creates the output directory if needed and saves the cleaned data as a CSV without the index. 

On the provided sample data, the pipeline reduces 100 rows to 92 by removing two invalid ratings, two duplicates, two rows with missing values, and two outliers.

Example command:

bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

Output: 

22:56:20 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
22:56:20 INFO     src.utils — Input file validated: 'fixtures/sample_data.csv'
22:56:20 INFO     src.utils — Input file validated: 'config/config.yaml'
22:56:20 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
22:56:20 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
22:56:20 INFO     __main__ — Rows before validation: 100
22:56:20 WARNING  src.data_validator — rating contains invalid values at row 94
22:56:20 WARNING  src.data_validator — rating contains invalid values at row 95
22:56:20 DEBUG    src.data_validator — Valid Rows: 98
22:56:20 DEBUG    src.data_validator — Removed Rows: 2
22:56:20 INFO     __main__ — Rows after validation: 98
22:56:20 DEBUG    src.data_processor — 2 duplicate row(s) removed.
22:56:20 DEBUG    src.data_processor — 2 null row(s) removed.
22:56:20 DEBUG    src.data_processor — Method=iqr, threshold=1.5: 2 row(s) removed.
{'rows_before': 100, 'rows_after': 92, 'rows_removed': 8, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
22:56:20 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
22:56:20 INFO     __main__ — Saved cleaned data to output/clean.csv.
