import cv2
import pytesseract
import pandas as pd
import re
from datetime import datetime
import src.constants as constants


def extract_transactions_from_image(image_path, year = constants.default_year):
    raw_text = extract_text_from_image(image_path)
    lines = get_lines_after_total(raw_text)
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


def get_transactions_and_dates_images(image_path):
    image = cv2.imread(image_path)
    transactions_image = crop_transactions(image)
    dates_image = crop_dates(image)
    transactions_with_dates_image = crop_transactions_with_dates(image)

    return {
        'transactions': transactions_image,
        'dates': dates_image,
        'transactions_with_dates': transactions_with_dates_image
    }


def crop_transactions_with_dates(image):
    height, width = image.shape[:2]
    crop_height = int(height * 0.8)  
    return image[:height - crop_height, :]


def crop_dates(image):
    height, width = image.shape[:2]
    crop_width = int(width * 0.2)  
    return image[:, crop_width:]


def crop_transactions(image):
    height, width = image.shape[:2]
    crop_width = int(width * 0.2)  
    return image[:, :width - crop_width]


def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    raw_text = pytesseract.image_to_string(gray)
    return raw_text.strip()


def get_lines_after_total(raw_text):
    lines = raw_text.split("\n")
    total_index = next((i for i, line in enumerate(lines) if "Ukupan iznos" in line), None)
    
    if total_index is not None:
        return lines[total_index + 2:]
    return []


