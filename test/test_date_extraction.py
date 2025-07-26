import unittest
from unittest.mock import patch
import numpy as np
from src.transactions import get_list_of_dates, get_list_of_formatted_dates

class TestDateExtraction(unittest.TestCase):
    def setUp(self):
        self.dates_image = np.zeros((1, 1))  # Placeholder for the image data
        self.year = 2023

    @patch('src.transactions.extract_text_from_image')
    def test_get_list_of_dates(self, mock_extract_text):
        #Setup
        mock_extract_text.return_value = "12\nSVI\n10\nSVI\n10\nSVI"

        # When
        dates = get_list_of_dates(self.dates_image)

        # Then
        expected_dates = [('12', 'SVI'), ('10', 'SVI'), ('10', 'SVI')]
        self.assertEqual(dates, expected_dates)

    @patch('src.transactions.get_list_of_dates')
    def test_get_list_of_formatted_dates(self, mock_get_list_of_dates):
        # Setup
        mock_get_list_of_dates.return_value = [('12', 'SVI'), ('10', 'SVI'), ('10', 'SVI')]

        # When
        formatted_dates = get_list_of_formatted_dates(self.dates_image, self.year)

        # Then
        expected_formatted_dates = ["2023-05-12", "2023-05-10", "2023-05-10"]
        self.assertEqual(formatted_dates, expected_formatted_dates)

