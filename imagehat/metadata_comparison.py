# NOTE: This is a base skeleton that works as a placekeeper for future improvement (or deletion)
# This will probably not work.


import os
from imagehat.parsers.jpeg_parser import JPEGParser


class MetadataComparison:
    """
    A class to extract and compare metadata from multiple images using different parsers.
    """

    PARSER_MAPPING = {
        ".jpg": "JPEGParser",
        ".jpeg": "JPEGParser",
        #     ".heic": "HEICParser",
        #     ".nef": "NEFParser",
    }

    def __init__(self, parsers):
        """
        Initialize with available parsers.

        :param parsers: A dictionary of available parsers {'JPEG': JPEGParser(), 'HEIC': HEICParser()}.
        :type parsers: dict
        """
        self.parsers = parsers  # Store available parsers

    def _get_parser(self, file_path):
        """
        Identify the correct parser based on file extension.

        :param file_path: Path to the image file.

        :return: Corresponding parser instance or None if unsupported.
        """
        ext = os.path.splitext(file_path)[1].lower()
        parser_class = self.PARSER_MAPPING.get(ext)

        if parser_class and parser_class in self.parsers:
            return self.parsers[parser_class]
        return None  # Unsupported format

    def extract_metadata(self, image_path):
        """
        Extract metadata using the appropriate parser.

        :param image_path: Path to the image file.
        :return: Extracted metadata or None if no parser is found.
        """
        parser = self._get_parser(image_path)

        if not parser:
            print(f"No parser available for: {image_path}")
            return None

        return parser.extract_metadata(image_path)

    @classmethod
    def metadata_comparison(cls, folder_path=None, list_of_images=None):
        """
        Extracts and compares EXIF metadata from multiple images, using the first image as a pivot.

        :param folder_path: Path to a folder containing images.
        :param list_of_images: List of ImageHat instances.
        :return: Dictionary containing ordered EXIF data across images.
        """
        if not folder_path and not list_of_images:
            raise ValueError("Either folder_path or list_of_images must be provided.")

        if folder_path and not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path.")

        # Identify image files and their parsers
        image_files = []
        if folder_path:
            image_files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if os.path.splitext(f)[1].lower() in cls.PARSER_MAPPING
            ]
        else:
            if not all(isinstance(img, JPEGParser) for img in list_of_images):
                raise ValueError(
                    "All elements in list_of_images must be ImageHat instances."
                )
            image_files = [img.path for img in list_of_images]

        if len(image_files) < 2:
            raise ValueError(
                "At least two images are required for metadata comparison."
            )

        # Extract metadata
        image_reports = []
        for image in image_files:
            parser = cls._get_parser(cls, image)
            if parser:
                metadata = parser.extract_metadata(image)
                if metadata:
                    image_reports.append(metadata)
            else:
                print(f"No parser found for {image}")

        # Use the first image's metadata as the pivot
        pivot_metadata = (
            image_reports[0]
            .get("APP1 Info", {})
            .get("EXIF Info", {})
            .get("EXIF Data", {})
        )
        if not pivot_metadata:
            raise ValueError("No EXIF metadata found in the first image.")

        metadata_records = {tag: [] for tag in pivot_metadata.keys()}

        # Compare metadata across all images
        for report in image_reports:
            exif_data = (
                report.get("APP1 Info", {}).get("EXIF Info", {}).get("EXIF Data", {})
            )
            for tag in metadata_records:
                metadata_records[tag].append(
                    exif_data.get(tag, None)
                )  # Use None if tag is missing

        return metadata_records
