import os
import struct
from typing import Union
from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, img_path: str):
        self.img_path: str = img_path  # Stores image path
        self.validate_file_path()  # Ensures the file exists and is supported
        self.binary_repr: bytes = self.get_binary_data()  # Reads binary data
        self.file_info: Union[None, dict] = None  # Stores file info

    def validate_file_path(self) -> None:
        """Validates the file path to ensure it exists and has a valid format."""
        if not isinstance(self.img_path, str):
            raise TypeError("File path must be a string.")

        if not os.path.exists(self.img_path):
            raise FileNotFoundError(f"File '{self.img_path}' does not exist.")

    
    def get_binary_data(self) -> bytes:
        """Reads the image file as a binary byte stream."""
        try:
            with open(self.img_path, "rb") as binary_repr:
                return binary_repr.read()
        except Exception as e:
            raise RuntimeError(f"Error reading file: {e}") from e

    @abstractmethod
    def generate_report(self):
        """Stub method for subclasses to implement specific metadata extraction."""
        raise NotImplementedError("Subclasses must implement `generate_report`.")
