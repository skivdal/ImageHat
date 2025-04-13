import os
import os.path
import struct

from imagehat.identifiers.extensions import VIDEO_EXTENSIONS


class MP4Parser:

    def __init__(self, video_path: str):
        self.video_path: str = video_path
        self._validate_file_path()
        self.binary_repr: bytes = (
            self.get_binary_data()
        )  # creates hexadecimal representaion
        self._atoms = []  # or: self._boxes
        # Metadata fields
        self.file_info: dict | None = None      # General file-level info (duration, brand, size...)
        self.moov_info: dict | None = None      # 'moov' atom info (important for structure and metadata)
        self.ilst_info: dict | None = None      # iTunes-style metadata container ('ilst')
        self.udta_info: dict | None = None      # User metadata (often found in 'udta' under 'moov')
        self.exif_info: dict | None = None      # Optional: found inside 'moov' > 'trak' > 'meta' boxes


    def get_binary_data(self) -> bytes:
        """
        Method for fetching image data as binary array.

        :return: Image files in binary representation.
        :rtype: bytes
        """
        try:
            with open(self.video_path, "rb") as binary_repr:
                binary_content: bytes = binary_repr.read()
                return (
                    binary_content
                    if isinstance(binary_content, bytes)
                    else binary_content.tobytes()
                )
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}") from e

    def _validate_files_path(self) -> None:
        if not isinstance(self.video_path, str):
            raise TypeError("Path must be a string.")

        _, ext = os.path.splitext(self.video_path)
        if ext.lower() not in VIDEO_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension '{ext}'. Supported formats: .mp4, .mov."
            )

        try:
            with open(self.video_path, "rb") as f:
                header = f.read(12)
                if b"ftyp" not in header:
                    raise ValueError("Invalid MP4/MOV file. 'ftyp' box not found.")
        except Exception as e:
            raise RuntimeError(f"Error reading video file: {e}") from e
    
    @classmethod
    def help(cls) -> None:
        """
        Prints help for class overview and method usage.

        Example usage:
            >>> ImageHat.help()
        """
        print(help(cls))
        print(cls.__doc__.strip())
        print(cls.help.__doc__.strip())

    def segment_data(self, end: int, start: int | None = None) -> None:
        """
        Metod for printing the whole byte array. Should be avoided as printed byte arrays are living nightmares.

        :return: a segment of self.binary_repr
        """
        if start is None:
            return self.binary_repr[:end]
        return self.binary_repr[start:end]

