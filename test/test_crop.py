import unittest
from unittest.mock import patch
import numpy as np
import src.util.crop as crop_util

class TestUtilFunctions(unittest.TestCase):
    original_image_shape = (1000, 1000, 3)
    original_image = np.zeros(original_image_shape, dtype=np.uint8)

    @patch("cv2.imread")
    def test_extract_bottom_80_percent_of_the_image(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = crop_util.extract_bottom_part_of_image(image, percentage=0.8)
        self.assertEqual(cropped.shape[0], 800)

    @patch("cv2.imread")
    def test_extract_right_70_percent_part_of_the_image(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = crop_util.extract_right_part_of_image(image, percentage=0.7)
        self.assertEqual(cropped.shape[1], 700) 

    @patch("cv2.imread")
    def test_extract_right_80_percent_part_of_the_image(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = crop_util.extract_right_part_of_image(image, percentage=0.8)
        self.assertEqual(cropped.shape[1], 800)

    @patch("cv2.imread")
    def test_extract_left_30_percent_of_the_image(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = crop_util.extract_left_part_of_image(image, percentage=0.3)
        self.assertEqual(cropped.shape[1], 300) 

    @patch("cv2.imread")
    def test_extract_left_80_percent_of_the_image(self, mock_imread):
        mock_imread.return_value = self.original_image
        image = mock_imread.return_value
        cropped = crop_util.extract_left_part_of_image(image, percentage=0.8)
        self.assertEqual(cropped.shape[1], 800)

if __name__ == '__main__':
    unittest.main()