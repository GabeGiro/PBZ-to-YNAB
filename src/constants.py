DATE_REGEX = r'(\d{1,2})\s+([A-ZČŽŠ]{3})'
AMOUNT_REGEX = r'([-+]?\d+,\d+)\s*EUR'
OUTPUT_DATE_FORMAT = '%Y-%m-%d'
ISOLATED_I_REGEX = r'\bI\b' 
ISOLATED_I_REPLACEMENT = '11'
ZERO_AMOUNT_REGEX = r'\b000,00\b'
ZERO_AMOUNT_REPLACEMENT = '+1000,00'
TIL_MINUS_REGEX = r'(?<=-)[Tt][1IilL][1IilL](?=,)'
TIL_PLUS_REGEX = r'(?<=\+)[Tt][1IilL][1IilL](?=,)'
TIL_ISOLATED_REGEX = r'\b[Tt][1IilL][1IilL](?=,)'
TIL_REPLACEMENT = '11'

# Month mapping for Croatian
month_map = {
    "SIJ": 1, "VEL": 2, "OŽU": 3, "TRA": 4, "SVI": 5, "LIP": 6, 
    "SRP": 7, "KOL": 8, "RUJ": 9, "LIS": 10, "STU": 11, "PRO": 12
}

total_match = "Ukupan iznos"
default_year = 2025
default_month = 4  