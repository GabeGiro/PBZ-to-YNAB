# PBZ-to-YNAB


## Project Setup

### Instal virtual environment

Recommended python version: 3.12

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Ignore Jupyter Notebook output
To ignore the output of Jupyter Notebooks use the following steps:

1. Install `nbstripout`:
   ```bash
   pip install nbstripout
   ```
2. Initialize `nbstripout` in your repository:
   ```bash
   nbstripout --install
   ```

### Run Tests
To run the tests, use the following command:

```bash
python -m unittest test.test_util
```

To run all tests, use:
```bash
python -m unittest discover 
```

### Open Jupyter Notebooks
To open Jupyter Notebooks, use the following command:
```bash
jupyter notebook
```

## Flow of converting PBZ screenshots of transactions to csv format

1. **Screenshot**: Take screenshots of the PBZ MyWay app showing the transactions.
2. **Upload**: Upload the screenshots to the data/sensitive/run directory.
   - Ensure the images are in PNG format and named appropriately.
3. **Screenshot to CSV Conversion**: To convert the screenshots to CSV format, run the OCR transaction extractor:
   ```bash
   python -m src.main
   ```
   - This will process the images and extract transaction data to a CSV file.
4. **Check Output**: The output CSV file will be saved in the data/sensitive/run directory.
   - The file will be named `transactions.csv` by default.
4. **Review**: Review the extracted data for accuracy. Check 01 and 11 dates and ensure that the transactions are correctly formatted.
   - If there are any issues, you may need to adjust the image or the extraction logic.
5. **CSV to YNAB Conversion**: Upload the CSV file to https://aniav.github.io/ynab-csv/
   - Follow the instructions on the website to convert the CSV file to a format compatible with YNAB.
6. **Import to YNAB**: Import the converted CSV file into your YNAB account.