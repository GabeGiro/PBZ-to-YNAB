import unittest
from unittest.mock import patch
import numpy as np
from src.transactions import get_list_of_descriptions, get_list_of_formatted_descriptions

class TestDescriptionExtraction(unittest.TestCase):
    def setUp(self):
        self.transactions_image = np.zeros((1, 1))  # Placeholder for the image data

    @patch('src.transactions.extract_text_from_image')
    def test_get_list_of_multiple_descriptions(self, mock_extract_text):
        # Setup
        mock_extract_text.return_value = "Payment for groceries\n11,00 EUR\nTransfer to savings\n\n11,00 EUR"

        # When
        descriptions = get_list_of_descriptions(self.transactions_image)

        # Then
        expected_descriptions = ["Payment for groceries", "Transfer to savings"]
        self.assertEqual(descriptions, expected_descriptions)

    @patch('src.transactions.extract_text_from_image')
    def test_get_list_of_multiline_descriptions(self, mock_extract_text):
        # Setup
        mock_extract_text.return_value = "Payment for groceries\nfrom the store\n11,00 EUR\nTransfer to savings\n\n11,00 EUR"

        # When
        descriptions = get_list_of_descriptions(self.transactions_image)

        # Then
        expected_descriptions = ["Payment for groceries from the store", "Transfer to savings"]
        self.assertEqual(descriptions, expected_descriptions)

    @patch('src.transactions.get_list_of_descriptions')
    def test_get_list_of_formatted_descriptions(self, mock_get_list_of_descriptions):
        # Setup
        mock_get_list_of_descriptions.return_value = ["Payment for groceries", "Transfer to savings"]

        # When
        formatted_descriptions = get_list_of_formatted_descriptions(self.transactions_image)

        # Then
        expected_formatted_descriptions = ["Payment for groceries", "Transfer to savings"]
        self.assertEqual(formatted_descriptions, expected_formatted_descriptions)

    @patch('src.transactions.extract_text_from_image')
    def test_edge_case_of_empty_description(self, mock_extract_text):
        # Setup
        mock_extract_text.return_value = ""

        # When
        descriptions = get_list_of_descriptions(self.transactions_image)

        # Then
        expected_descriptions = []
        self.assertEqual(descriptions, expected_descriptions)

    @patch('src.transactions.get_list_of_descriptions')
    def test_extracting_description_with_EUROPE_word(self, mock_get_list_of_descriptions):
        # Setup
        mock_get_list_of_descriptions.return_value = ["Payment for groceries in EUROPE", "Transfer to savings"]

        # When
        formatted_descriptions = get_list_of_formatted_descriptions(self.transactions_image)

        # Then
        expected_formatted_descriptions = ["Payment for groceries in EUROPE", "Transfer to savings"]
        self.assertEqual(formatted_descriptions, expected_formatted_descriptions)