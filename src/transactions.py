import cv2
import pytesseract
import pandas as pd
import re
from datetime import datetime
import src.constants as constants
import src.util.crop as crop_util
from src.data.image import ImageData
from src.data.transaction import Transaction


def extract_transactions_from_image(image_path, year=constants.default_year):
    cropped_images = get_cropped_dates_and_transactions_images(image_path)
    if not is_number_of_rows_matching(cropped_images.dates_image, cropped_images.transactions_image):
        raise ValueError("The number of dates, amounts, and descriptions do not match. Please check the input image.")
    
    transactions = get_list_of_transactions(
        dates_image=cropped_images.dates_image,
        transactions_image=cropped_images.transactions_image,
        year=year
    )

    return pd.DataFrame(transactions)


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


def get_list_of_formatted_dates(dates_image, year):
    dates = get_list_of_dates(dates_image)
    formatted_dates = []

    for day, month_abbr in dates:
        month = constants.month_map.get(month_abbr.upper(), constants.default_month)
        formatted_date = datetime(year, month, int(day)).strftime(constants.OUTPUT_DATE_FORMAT)
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
    current_description = ""

    for line in lines:
        if "EUR" in line:
            if current_description.strip():
                descriptions.append(current_description.strip())
            current_description = ""  # Reset for the next description
        else:
            current_description += f" {line.strip()}"

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


def get_list_of_transactions(dates_image, transactions_image, year):
    dates = get_list_of_formatted_dates(dates_image, year)
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

