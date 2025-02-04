import unittest
import os
import random
from imagehat.__main__  import ImageHat

# Define test image directory
DIR = "./tests/testsets/testset-small"
IMG = random.choice(os.listdir(DIR))

class TestImageHat(unittest.TestCase):

    def setUp(self):
        """
        Set up test files and ensure a clean test environment.
        This runs before each test.
        """
        self.valid_image_path = os.path.join(DIR, IMG)   # Random valid image
        self.invalid_image_path = "tests/nonexistent.jpg"  # Non-existent file
        self.invalid_format_path = "tests/sample.txt"  # Invalid file type
        self.empty_image_path = "tests/empty.jpg"  # Empty file
        self.corrupt_image_path = "tests/corrupt.jpg"  # Corrupt file

        with open(self.empty_image_path, "wb") as f:
            f.write(b"")

        with open(self.corrupt_image_path, "wb") as f:
            f.write(b"\xFF\xD8")  # Start of Image (SOI) but missing data

    def tearDown(self):
        """
        Clean up temporary test files after execution.
        This runs after each test.
        """
        for file in [self.empty_image_path, self.corrupt_image_path, self.invalid_format_path]:
            if os.path.exists(file):
                os.remove(file)



    def test_constructor_valid_file(self):
        """
        Test if ImageHat initializes properly with a valid image.
        """
        img = ImageHat(self.valid_image_path)
        self.assertEqual(img.img_path, self.valid_image_path)

    def test_valid_image_load(self):
        """Test if a valid image loads properly."""
        img = ImageHat(self.valid_image_path)
        self.assertIsInstance(img.binary_image, bytes)
        self.assertGreater(len(img.binary_image), 0)

    def test_invalid_file_path(self):
        """Test if a missing file raises an error."""
        with self.assertRaises(FileNotFoundError):
            ImageHat(self.invalid_image_path)

    def test_invalid_file_format(self):
        """Test if an unsupported file format raises an error."""
        with open(self.invalid_format_path, "w") as f:
            f.write("This is a text file, not an image.")

        with self.assertRaises(ValueError):
            ImageHat(self.invalid_format_path)

        os.remove(self.invalid_format_path)

    ### ✅ ADVANCED FUNCTIONALITY TESTS ###

    def test_find_jpeg_segments(self):
        """Test if JPEG markers are correctly identified."""
        img = ImageHat(self.valid_image_path)
        segments = img.find_jpeg_segments()

        self.assertIsInstance(segments, dict)
        self.assertGreaterEqual(len(segments), 1)  # Ensure at least one marker exists

    def test_find_app1_segment(self):
        """Test if the APP1 segment is correctly located."""
        img = ImageHat(self.valid_image_path)
        app1_segment = img.find_app1_segment()

        if isinstance(app1_segment, dict):  # Only run assertions if a valid segment is found
            self.assertIn("start_position", app1_segment)
            self.assertIn("length", app1_segment)
            self.assertGreater(app1_segment["length"], 0)

    def test_verify_type_image(self):
        """Test if verify_type_image correctly detects EXIF or TIFF metadata."""
        img = ImageHat(self.valid_image_path)
        
        try:
            img.verify_type_image()  # This should not raise an error
        except ValueError:
            self.fail("verify_type_image() raised ValueError unexpectedly.")

    ### ✅ EDGE CASE TESTS ###

    def test_empty_image_file(self):
        """Test if an empty image file is handled properly."""
        with self.assertRaises(ValueError):
            ImageHat(self.empty_image_path)

    def test_corrupt_image_file(self):
        """Test if a corrupt image file (incomplete JPEG) is handled properly."""
        img = ImageHat(self.corrupt_image_path)
        self.assertIsInstance(img.binary_image, bytes)
        self.assertLess(len(img.binary_image), 10)  # Should be very small

    def test_string_representation(self):
        """Test the __str__() method of ImageHat."""
        img = ImageHat(self.valid_image_path)
        output = str(img)

        self.assertIn("ImageHat:", output)
        self.assertIn(self.valid_image_path, output)
        self.assertTrue("Size:" in output)

if __name__ == '__main__':
    unittest.main()
