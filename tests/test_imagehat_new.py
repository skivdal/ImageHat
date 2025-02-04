import pytest
import os
import random
from imagehat.__main__ import ImageHat  # Ensure correct module import

# Define test image directory
DIR = "./tests/testsets/testset-small"

# Get a random valid test image from testset-small
IMG = random.choice(os.listdir(DIR))


@pytest.fixture
def setup_files():
    """
    Fixture that creates test files and cleans them up after tests.
    """
    paths = {
        "valid_image_path": os.path.join(DIR, IMG),   # Random valid image
        "invalid_image_path": "tests/nonexistent.jpg",  # Non-existent file
        "invalid_format_path": "tests/sample.txt",  # Invalid file type
        "empty_image_path": "tests/empty.jpg",  # Empty file
        "corrupt_image_path": "tests/corrupt.jpg"  # Corrupt file
    }

