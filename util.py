import cv2
import pytesseract
import pandas as pd
import re
from datetime import datetime
import constants


# 📥 OCR + Regex Parser Function
def extract_transactions_from_image(image_path, year = constants.default_year):
    raw_text = extract_text_from_image(image_path)

    # Parse lines
    lines = raw_text.split("\n")
    data = []
    current_date = ""

    for i, line in enumerate(lines):
        date_match = re.match(constants.DATE_REGEX, line.strip())
        if date_match:
            day, month_abbr = date_match.groups()
            day = int(day)
            month = constants.month_map.get(month_abbr.upper(), constants.default_month)
            current_date = datetime(year, month, day).strftime(constants.OUTPUT_DATE_FORMAT)
        elif "EUR" in line:
            amount_match = re.search(constants.AMOUNT_REGEX, line)
            if amount_match and i > 0:
                amount = amount_match.group(1).replace(',', '.')
                try:
                    prev_line = lines[i - 1].strip()
                    data.append({
                        'Date': current_date,
                        'Description': prev_line,
                        'Amount (EUR)': float(amount)
                    })
                except:
                    pass

    return pd.DataFrame(data)


def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # OCR extraction
    raw_text = pytesseract.image_to_string(gray)
    return raw_text.strip()


def get_lines_without_total(raw_text):
    lines = raw_text.split("\n")
    # remove first line
    if lines and lines[0].strip():
        lines = lines[1:]
    return lines
