import cv2
import pytesseract
import pandas as pd
import re
from datetime import datetime
import src.constants as constants
import src.util.crop as crop_util
from src.data.image import ImageData
from src.data.transaction import Transaction


def extract_transactions_from_image(image_path, year = constants.default_year):
    image = cv2.imread(image_path)
    raw_text = extract_text_from_image(image)
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


def get_cropped_dates_and_transactions_images(image_path):
    image = cv2.imread(image_path)
    dates_and_transactions_image = crop_transactions_and_dates(image)
    if dates_and_transactions_image is None:
        raise ValueError("Failed to crop the image. Please check the input image.")
    transactions_image = get_cropped_transactions_image(dates_and_transactions_image)
    dates_image = get_cropped_dates_image(dates_and_transactions_image)

    return ImageData(
        transactions_image=transactions_image,
        dates_image=dates_image
    )


def crop_transactions_and_dates(image):
    return crop_util.extract_bottom_part_of_image(image, percentage=0.7)


def get_cropped_dates_image(image):
    return crop_util.extract_left_part_of_image(image, percentage=0.2)


def get_cropped_transactions_image(image):
    return crop_util.extract_right_part_of_image(image, percentage=0.8)


def get_list_of_dates(dates_image):
    raw_text = extract_text_from_image(dates_image)
    date_pattern = constants.DATE_REGEX
    dates = re.findall(date_pattern, raw_text)
    return dates


def get_list_of_formatted_dates(dates_image):
    dates = get_list_of_dates(dates_image)
    formatted_dates = []

    for day, month_abbr in dates:
        month = constants.month_map.get(month_abbr.upper(), constants.default_month)
        formatted_date = datetime(constants.default_year, month, int(day)).strftime(constants.OUTPUT_DATE_FORMAT)
        formatted_dates.append(formatted_date)

    return formatted_dates


def count_number_of_dates(dates_image):
    dates = get_list_of_dates(dates_image)
    return len(dates)


def get_list_of_amounts(transactions_image):
    raw_text = extract_text_from_image(transactions_image)
    transaction_pattern = constants.AMOUNT_REGEX
    transactions = re.findall(transaction_pattern, raw_text)
    return transactions


def get_list_of_formatted_amounts(transactions_image):
    transactions = get_list_of_amounts(transactions_image)
    formatted_transactions = []

    for amount in transactions:
        amount = amount.replace(',', '.')
        try:
            formatted_transactions.append(float(amount))
        except ValueError:
            continue

    return formatted_transactions


def count_number_of_amounts(transactions_image):
    transactions = get_list_of_amounts(transactions_image)
    return len(transactions)


def get_list_of_descriptions(transactions_image):
    raw_text = extract_text_from_image(transactions_image)
    lines = raw_text.split("\n")
    descriptions = []

    for i, line in enumerate(lines):
        if "EUR" in line and i > 0:
            description = lines[i - 1].strip()
            if description:
                descriptions.append(description)

    return descriptions


def get_list_of_formatted_descriptions(transactions_image):
    descriptions = get_list_of_descriptions(transactions_image)
    formatted_descriptions = []

    for description in descriptions:
        if description:
            formatted_descriptions.append(description)

    return formatted_descriptions


def count_number_of_descriptions(transactions_image):
    descriptions = get_list_of_descriptions(transactions_image)
    return len(descriptions)


def get_list_of_transactions(dates_image, transactions_image):
    dates = get_list_of_formatted_dates(dates_image)
    amounts = get_list_of_formatted_amounts(transactions_image)
    descriptions = get_list_of_formatted_descriptions(transactions_image)

    transactions = []
    for date, amount, description in zip(dates, amounts, descriptions):
        transactions.append(
            Transaction(
                date=date, 
                amount=amount, 
                description=description
            )
        )

    return transactions


def is_number_of_rows_matching(dates_image, transactions_image):
    number_of_dates = count_number_of_dates(dates_image)
    number_of_transactions = count_number_of_amounts(transactions_image)
    number_of_descriptions = count_number_of_descriptions(transactions_image)
    return number_of_dates == number_of_transactions == number_of_descriptions


def extract_text_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    raw_text = pytesseract.image_to_string(gray)
    return raw_text.strip()


def get_lines_after_total(raw_text):
    lines = raw_text.split("\n")
    total_index = next((i for i, line in enumerate(lines) if constants.total_match in line), None)
    
    if total_index is not None:
        return lines[total_index + 2:]
    return []


