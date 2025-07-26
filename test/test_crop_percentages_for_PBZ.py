import unittest
from unittest.mock import patch
import numpy as np
from src.transactions import get_cropped_dates_and_transactions_images, crop_transactions_and_dates, get_cropped_transactions_image, get_cropped_dates_image
from src.data.image import ImageData

class TestCropImageFunctions(unittest.TestCase):
    original_image_shape = (1000, 1000, 3)
    original_image = np.zeros(original_image_shape, dtype=np.uint8)

    @patch('cv2.imread')
    def test_get_transactions_and_dates_images(self, mock_imread):
        mock_imread.return_value = self.original_image
        result = get_cropped_dates_and_transactions_images("test_image.png")
        self.assertIsInstance(result, ImageData)
        self.assertEqual(result.dates_image.shape, (700, 200, 3))
        self.assertEqual(result.transactions_image.shape, (700, 800, 3))

    @patch('cv2.imread')
    def test_crop_transactions_with_dates_should_reduce_height_by_30_percent(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = crop_transactions_and_dates(image)
        self.assertEqual(cropped.shape[0], 700) 

    @patch('cv2.imread')
    def test_crop_transactions_should_reduce_width_by_20_percent(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = get_cropped_transactions_image(image)
        self.assertEqual(cropped.shape[1], 800) 

    @patch('cv2.imread')
    def test_crop_dates_should_reduce_width_by_80_percent(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = get_cropped_dates_image(image)
        self.assertEqual(cropped.shape[1], 200) 

if __name__ == '__main__':
    unittest.main()