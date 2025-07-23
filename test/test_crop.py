import unittest
import numpy as np
import src.util.crop as crop_util

class TestUtilFunctions(unittest.TestCase):
    original_image_shape = (1000, 1000, 3)
    original_image = np.zeros(original_image_shape, dtype=np.uint8)

    def test_extract_bottom_80_percent_of_the_image(self):
        cropped = crop_util.extract_bottom_part_of_image(self.original_image, percentage=0.8)
        self.assertEqual(cropped.shape[0], 800)

    def test_extract_right_70_percent_part_of_the_image(self):
        cropped = crop_util.extract_right_part_of_image(self.original_image, percentage=0.7)
        self.assertEqual(cropped.shape[1], 700)

    def test_extract_right_80_percent_part_of_the_image(self):
        cropped = crop_util.extract_right_part_of_image(self.original_image, percentage=0.8)
        self.assertEqual(cropped.shape[1], 800)

    def test_extract_left_30_percent_of_the_image(self):
        cropped = crop_util.extract_left_part_of_image(self.original_image, percentage=0.3)
        self.assertEqual(cropped.shape[1], 300)

    def test_extract_left_80_percent_of_the_image(self):
        cropped = crop_util.extract_left_part_of_image(self.original_image, percentage=0.8)
        self.assertEqual(cropped.shape[1], 800)

if __name__ == '__main__':
    unittest.main()