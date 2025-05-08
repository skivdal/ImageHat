import os
import struct

from imagehat.parsers.base_parser import BaseParser
from imagehat.identifiers.extensions import VALID_EXTENSIONS
from imagehat.identifiers.png_identifiers import PNG_CHUNK_MARKERS, IDENTIFIERS


class WEBPParser(BaseParser):
    def __init__(self, img_path: str):
        self.img_path = img_path
        self._validate_file_path()
        self.binary_repr = self.get_binary_data()

        self.metadata = {}

    def get_binary_data(self) -> bytes:
        try:
            with open(self.img_path, "rb") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Could not read file '{self.img_path}': {e}") from e

    def _validate_file_path(self) -> None:
        """
        This method is used for validating the file paths, reducing the chance of error during initializing.
        Takes no parameters and is void.
        """
        if not isinstance(self.img_path, str):
            raise TypeError("Not valid type, must be string.")

        if not os.path.exists(self.img_path):
            raise FileNotFoundError(
                f"The file '{self.img_path}' does not exist or is located elsewhere."
            )

        _, ext = os.path.splitext(self.img_path)
        if ext.lower() not in VALID_EXTENSIONS:
            raise ValueError(f"Invalid file format '{ext}'. Supported formats: .webp")

        with open(self.img_path, "rb") as f:
                riff_header = f.read(4)
                if riff_header != b'RIFF':
                    raise ValueError("[ERROR] Not a valid WEBP (missing RIFF header)")


    def get_complete_image_data(self):
        return super().get_complete_image_data()
    
    def get_exif_image_data(self):
        return super().get_exif_image_data()

    @classmethod
    def get_image_datas(
        cls, images: str | list, verbose: str = "complete", limit=None, segment=None
    ) -> list[dict]:
        pass



if __name__ == "__main__":
    path = r"datasets\scraped_news_images\downloaded_images\Forskning.no\2020369.webp"
    path = r"datasets\scraped_news_images\downloaded_images\Forskning.no\2487640.webp"

    # img = WEBPParser(path)
    # print(img.get_complete_image_data())
    # print(img.binary_repr[:100])
    with open(path, "rb") as file:
        data = file.read()

    print(data[:100])
