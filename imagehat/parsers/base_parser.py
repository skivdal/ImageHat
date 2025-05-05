# imagehat/parsers/base_parser.py

from abc import ABC, abstractmethod


class BaseParser(ABC):
    def __init__(self, img_path: str):
        self.img_path = img_path
        self.binary_repr = self.get_binary_data()

        self.png_chuncks = None

    def __str__(self) -> str:
        """
        Returns a summary of the parsed image.
        """
        return f"Image: {self.img_path}, Size: {len(self.binary_repr)} bytes"

    @classmethod
    def help(cls) -> None:
        """
        Prints help for class overview and method usage.

        Example usage:
            >>> ParserClass.help()
        """
        print(help(cls))
        if cls.__doc__:
            print(cls.__doc__.strip())
        if cls.help.__doc__:
            print(cls.help.__doc__.strip())

    def segment_data(self, end: int, start: int | None = None) -> bytes:
        """
        Returns a segment of the binary representation of the file.

        :param end: End byte offset.
        :param start: Start byte offset (optional).
        """
        if start is None:
            return self.binary_repr[:end]
        return self.binary_repr[start:end]

    @abstractmethod
    def _validate_file_path(self):
        """
        Validates the file path and extension. Each parser may apply its own rules.
        """
        pass

    @abstractmethod
    def get_exif_image_data(self) -> dict:
        """
        Return only EXIF-related metadata (or similar for formats that support it).
        """
        pass

    @abstractmethod
    def get_complete_image_data(self) -> dict:
        """
        Return the full metadata report (format-specific), including general file info and markers/chunks.
        """
        pass

    @classmethod
    @abstractmethod
    def get_image_datas(
        cls,
        images: str | list,
        verbose: str = "complete",
        limit=None,
        segment=None,
    ) -> list[dict]:
        """
        Batch processing of multiple images in a folder or list.

        :param images: Folder path or list of image paths.
        :param verbose: 'complete' or 'exif' mode.
        :param limit: Limit number of files.
        :param segment: Tuple to define a subrange.
        """
        pass
