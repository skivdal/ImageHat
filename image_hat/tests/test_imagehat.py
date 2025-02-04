import unittest
import os
from __main__ import ImageHat

class TestImageHat(unittest.TestCase):

    def setUp(self):
        """Set up a test image file and ImageHat instance."""

        self.valid_image_path = r"tests/testset"  # Replace with an actual test image path
        self.invalid_image_path = "tests/nonexistent.jpg"
        self.invalid_format_path = "tests/sample.txt"
