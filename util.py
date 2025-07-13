import cv2
import pytesseract
import pandas as pd
import re
from datetime import datetime

# You may need to specify the tesseract path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Month mapping for Croatian
month_map = {
    "SIJ": 1, "VEL": 2, "OŽU": 3, "TRA": 4, "SVI": 5,
    "LIP": 6, "SRP": 7, "KOL": 8, "RUJ": 9, "LIS": 10,
    "STU": 11, "PRO": 12
}

# 📥 OCR + Regex Parser Function
def extract_transactions_from_image(image_path, year=2025):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # OCR extraction
    raw_text = pytesseract.image_to_string(gray)

    # Parse lines
    lines = raw_text.split('\n')
    data = []
    current_date = ""

    for i, line in enumerate(lines):
        date_match = re.match(r'(\d{1,2})\s+([A-ZČŽŠ]{3})', line.strip())
        if date_match:
            day, month_abbr = date_match.groups()
            day = int(day)
            month = month_map.get(month_abbr.upper(), 4)  # default to April
            current_date = datetime(year, month, day).strftime('%Y-%m-%d')
        elif "EUR" in line:
            amount_match = re.search(r'([-+]?\d+,\d+)\s*EUR', line)
            if amount_match and i > 0:
                amount = amount_match.group(1).replace(',', '.')
                try:
                    prev_line = lines[i-1].strip()
                    data.append({
                        'Date': current_date,
                        'Description': prev_line,
                        'Amount (EUR)': float(amount)
                    })
                except:
                    pass

    return pd.DataFrame(data)

