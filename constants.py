DATE_REGEX = r'(\d{1,2})\s+([A-ZČŽŠ]{3})'
AMOUNT_REGEX = r'([-+]?\d+,\d+)\s*EUR'
OUTPUT_DATE_FORMAT = '%Y-%m-%d'

# Month mapping for Croatian
month_map = {
    "SIJ": 1, "VEL": 2, "OŽU": 3, "TRA": 4, "SVI": 5, "LIP": 6, 
    "SRP": 7, "KOL": 8, "RUJ": 9, "LIS": 10, "STU": 11, "PRO": 12
}

default_year = 2025
default_month = 4  