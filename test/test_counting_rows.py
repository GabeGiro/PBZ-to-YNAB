import unittest
import numpy as np
from unittest.mock import patch
from src.transactions import count_number_of_dates, count_number_of_descriptions, count_number_of_amounts, is_number_of_rows_matching

class TestCountingFunctions(unittest.TestCase):
    def setUp(self):
        self.dates_image = np.zeros((1, 1))
        self.transactions_image = np.zeros((1, 1))
        self.year = 2023

    @patch('src.transactions.count_number_of_dates')
    @patch('src.transactions.count_number_of_descriptions')
    @patch('src.transactions.count_number_of_amounts')
    def test_counting_rows_matches(self, mock_count_number_of_amounts, mock_count_number_of_descriptions, mock_count_number_of_dates):
        # Setup
        mock_count_number_of_amounts.return_value = 5
        mock_count_number_of_descriptions.return_value = 5
        mock_count_number_of_dates.return_value = 5

        #When

        #Then
        self.assertTrue(is_number_of_rows_matching(dates_image=self.dates_image, transactions_image=self.transactions_image))

    
