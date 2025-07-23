import unittest
from unittest.mock import patch, MagicMock
import src.util as util

class TestUtilFunctions(unittest.TestCase):
    @patch('cv2.imread')
    @patch('cv2.cvtColor')
    @patch('pytesseract.image_to_string')
    def test_extract_text_from_image(self, mock_image_to_string, mock_cvtColor, mock_imread):
        # Mock the behavior of cv2 and pytesseract
        mock_imread.return_value = MagicMock()
        mock_cvtColor.return_value = MagicMock()
        mock_image_to_string.return_value = "Ukupan iznos\n27 TRA\n-21,92 EUR"

        result = util.extract_text_from_image("test_image.png")
        self.assertEqual(result, "Ukupan iznos\n27 TRA\n-21,92 EUR")

    def test_get_lines_after_total(self):
        raw_text = "Ukupan iznos\n27 TRA\n-21,92 EUR\n26 TRA\n-16,40 EUR"
        result = util.get_lines_after_total(raw_text)
        expected = ["26 TRA", "-16,40 EUR"]
        self.assertEqual(result, expected)

    @patch('cv2.imread')
    def test_get_transactions_and_dates_images(self, mock_imread):
        mock_imread.return_value = MagicMock(shape=(1000, 500, 3))
        result = util.get_transactions_and_dates_images("test_image.png")
        self.assertIn('transactions', result)
        self.assertIn('dates', result)
        self.assertIn('transactions_with_dates', result)

    @patch('cv2.imread')
    def test_crop_transactions(self, mock_imread):
        mock_imread.return_value = MagicMock(shape=(1000, 500, 3))
        image = mock_imread.return_value
        cropped = util.crop_transactions(image)
        self.assertEqual(cropped.shape[1], 400)  # Width reduced by 20%

    @patch('cv2.imread')
    def test_crop_dates(self, mock_imread):
        mock_imread.return_value = MagicMock(shape=(1000, 500, 3))
        image = mock_imread.return_value
        cropped = util.crop_dates(image)
        self.assertEqual(cropped.shape[1], 100)  # Width reduced by 20%

    @patch('cv2.imread')
    def test_crop_transactions_with_dates(self, mock_imread):
        mock_imread.return_value = MagicMock(shape=(1000, 500, 3))
        image = mock_imread.return_value
        cropped = util.crop_transactions_with_dates(image)
        self.assertEqual(cropped.shape[0], 200)  # Height reduced by 80%

if __name__ == '__main__':
    unittest.main()