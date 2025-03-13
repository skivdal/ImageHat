import os
import os.path
import struct
from identifiers.constants import (
    MARKER_SEGMENTS_JPEG_ADDRESS,
    MARKER_SEGMENTS_JPEG_NAME,
    IDENTIFIERS,
)
from identifiers.tag_support_levels import (
    TAG_TYPES,
    OVERFLOW_TYPES,
    EXIF_TAG_DICT,
)
from identifiers.valid_formats import VALID_FORMATS
from typing import Union


class ImageHat:
    """
    The ImageHat class is designed to analyze binary image files and extract EXIF metadata,
    and validat. It supports methods for reading JPEG markers,
    parsing EXIF data, and converting hex values.

    Example Usage:
    --------------
    >>> image = ImageHat("sample.jpg")
    >>> markers = image.get_image_data(verbose="exif")
    >>> print(markers)
    """

    def __init__(self, img_path):
        self.img_path: str = img_path  # stores the image adress / path
        self._validate_file_path()  # validates file path
        self.binary_repr: bytes = (
            self.get_binary_data()
        )  # creates hexadecimal representaion
        self._APP1_SEGMENT = None
        self.file_info: Union[None, dict] = None
        self.app1_info: Union[None, dict] = None
        self.exif_info: Union[None, dict] = None

    def get_binary_data(self) -> bytes:
        """
        Method for fetching image data as binary array.
        """
        try:
            with open(self.img_path, "rb") as binary_repr:
                binary_content: bytes = binary_repr.read()
                if not isinstance(binary_content, bytes):
                    binary_content = binary_content.tobytes()
                return binary_content
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}") from e

    def _validate_file_path(self) -> None:
        """
        This method is used for validating the file paths, reducing the chance of error during initializing.
        """
        if not isinstance(self.img_path, str):
            raise TypeError("Not valid type, must be string.")

        if not os.path.exists(self.img_path):
            raise FileNotFoundError(
                f"The file '{self.img_path}' does not exist or is located elsewhere."
            )

        _, ext = os.path.splitext(self.img_path)
        if ext.lower() not in {".jpg", ".jpeg"}:
            raise ValueError(
                f"Invalid file format '{ext}'. Supported formats: .jpg, .jpeg."
            )

        try:
            with open(self.img_path, "rb") as f:
                header = f.read(2)
                if (
                    header != MARKER_SEGMENTS_JPEG_NAME["SOI"]
                ):  # JPEG files start with 0xFFD8
                    raise ValueError("File is not a valid JPEG (missing SOI marker).")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {e}") from e

    # def validate_exif(self) -> None:
    #     """
    #     This method is for verifying that
    #     """
    #     if not MARKER_SEGMENTS_JPEG_NAME["APP1"] in self.binary_repr:
    #         raise ValueError(f"Binary image does not contain Application Layer 1. No EXIF data found.")

    #     if not IDENTIFIERS["IDENTIFIERS"] in self.binary_repr:
    #         raise ValueError(f"Binary image does not contain an EXIF identifier.")

    def __str__(self) -> str:
        return f"ImageHat: {self.img_path}, Size: {len(self.binary_repr)} bytes"

    def show_data(self) -> None:
        """
        Metod for printing the whole byte array. Should be avoided as printed byte arrays are living nightmares.
        """
        print(self.binary_repr)

    def _read_jpeg_markers(self) -> dict:
        """
        Locate all JPEG markers in the binary image, count occurrences,
        and return their offset.

        Returns:
            dict: A dictionary where keys are marker names and values are
                dictionaries with 'count' and 'offset'.
        """
        marker_info = {}

        for marker, name in MARKER_SEGMENTS_JPEG_ADDRESS.items():
            offset = []
            pos = self.binary_repr.find(marker)  # Find first occurrence

            while pos != -1:
                offset.append(pos)
                pos = self.binary_repr.find(marker, pos + 1)  # Find next occurrence

            if offset:  # Only store markers that were found
                marker_info[name] = {"count": len(offset), "offset": offset}
        return marker_info

    def _read_app1_segment(self, app1_offset) -> dict:
        """
        This method is used for locating the APP1 segment and recording information about its relative structure.
        """
        report = {}
        # Recording APP1 segment size (s.b. 2 bytes)
        app1_size = int.from_bytes(
            self.binary_repr[app1_offset + 2 : app1_offset + 4], byteorder="big"
        )
        report["APP1 Size"] = app1_size  # For latter, add failsafe if segment > 64 kb

        # Recording start of APP1 segment
        app1_location_start = app1_offset
        report["Start of APP1"] = app1_location_start

        # Recording end of APP1 segment
        app1_location_end = app1_offset + app1_size
        report["End of APP1"] = app1_location_end
        self._APP1_SEGMENT = self.binary_repr[
            app1_location_start : app1_location_start + app1_size
        ]

        # Recording EXIF identifier (s.b. 4 bytes, 6 bytes including padding)
        exif_identifier = self._APP1_SEGMENT.find(IDENTIFIERS["exif_identifier"])
        report["EXIF Identifier Offset"] = exif_identifier if exif_identifier else None

        # Recording byte order (s.b. 2 bytes)
        # Recodring endianness starts here. EXIF is big-endian until byte-order is discovered.
        byte_order_offset, endianness_report = self._find_target_byte(
            self._APP1_SEGMENT[:25], targets=[IDENTIFIERS["II"], IDENTIFIERS["MM"]]
        )
        byte_order_bytes = self._APP1_SEGMENT[byte_order_offset : byte_order_offset + 2]

        # Setting endianness for the rest of runtime
        endianness = "<" if byte_order_bytes == IDENTIFIERS["II"] else ">"
        report["Byte Order"] = endianness_report

        # Recording magic number (s.b. 2 bytes)
        magic_number = self._convert_internal_identifier(
            endianness, "H", "tiff_magic_number"
        )
        magic_number_offset = self._APP1_SEGMENT.find(magic_number)

        magic_number_bytes = self._APP1_SEGMENT[
            magic_number_offset : magic_number_offset + 2
        ]  # Read raw bytes
        magic_number = struct.unpack(f"{endianness}H", magic_number_bytes)[0]
        report["TIFF Magic Number"] = magic_number_bytes
        report["TIFF Magic Number Offset"] = magic_number_offset

        ### Extremely important NOTE. All markers and tags in the JEITA documentations are displayed in MSB.
        ### Always unpack constants in big endian from project files.
        comp_magic_number = struct.unpack(">H", IDENTIFIERS["tiff_magic_number"])[0]
        report["TIFF Validity"] = magic_number == comp_magic_number

        # Recording offset to first IDF (s.b. 4 bytes)
        ifd_temp = self._convert_internal_identifier(
            endianness=endianness, datatype="I", id="offset_first_ifd"
        )
        ifd_offset = self._APP1_SEGMENT.find(ifd_temp)
        ifd_offset_bytes = self._APP1_SEGMENT[ifd_offset : ifd_offset + 4]
        ifd_start = (
            byte_order_offset + struct.unpack(f"{endianness}I", ifd_offset_bytes)[0]
        )

        # Entries recorded within the 0th IFD
        ifd_entries = struct.unpack(
            f"{endianness}H", self._APP1_SEGMENT[ifd_start : ifd_start + 2]
        )[0]
        report["0th IFD bytes"] = ifd_offset_bytes
        report["0th IFD offset"] = ifd_offset
        report["0th IFD start"] = ifd_start
        report["Entries in 0th IFD"] = ifd_entries

        # Recording the EXIF tags. NOTE: Most important, do not touch.
        exif_information = self._read_exif_ifd(
            ifd_start=ifd_start,
            num_entries=ifd_entries,
            tiff_header_offset=byte_order_offset,
            endianness=endianness,
        )
        report["EXIF Info"] = exif_information

        return report

    def _find_target_byte(
        self, data: bytes, targets: Union[bytes, None]
    ) -> Union[None, int, str]:
        """
        Method that is used for finding the correct endianness with as little complexity as possible.
        """
        for target in targets:
            index = data.find(target)
            if index != -1:
                return index, target
        return None

    def _convert_internal_identifier(
        self, endianness: str, datatype: str, id: str
    ) -> bytes:
        """
        Method that mitigates errors caused by incosistent representation of byte sequences.
        """
        if id not in IDENTIFIERS:
            raise KeyError(
                f"Identifier '{id}' not found in IDENTIFIERS."
            )  # Raises key error if identifier not found

        if endianness == ">":
            return IDENTIFIERS[id]  # Big-endian

        unpacked_value = struct.unpack(f">{datatype}", IDENTIFIERS[id])[
            0
        ]  # Unpack in big-endian
        return struct.pack(
            f"{endianness}{datatype}", unpacked_value
        )  # Repack value according to correct endianness

    def _read_exif_ifd(
        self, ifd_start, num_entries, tiff_header_offset, endianness
    ) -> dict:
        """
        Reads and extracts all Exif IFD entries.
        """
        report = {}

        # This loop starts at the recorded start of the first ifd,
        # skips the 2 num_entries bytes, and iterates over each entry.
        exif_ifd_offset = None
        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry * 12)
            tag, datatype, count, value_offset = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )
            hex_tag = tag.to_bytes(2, "big")
            if hex_tag == IDENTIFIERS["exif_ifd_pointer"]:  # Exif IFD Pointer
                exif_ifd_offset = tiff_header_offset + value_offset
                report["Exif IFD pointer found"] = bool(tag)
                break

        if not exif_ifd_offset:
            return {"Exif IFD Pointer not found"}

        # Read number of entries in Exif IFD
        num_exif_entries = struct.unpack(
            f"{endianness}H", self._APP1_SEGMENT[exif_ifd_offset : exif_ifd_offset + 2]
        )[0]
        report["Number of Exif Entries"] = num_exif_entries

        # Extract key EXIF tags
        exif_data = {}

        # Iterate over the Exif specific IFD entries
        for i in range(num_exif_entries):
            entry_offset = exif_ifd_offset + 2 + (i * 12)  # Rec
            tag, datatype, count, value = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )

            tag_bytes = tag.to_bytes(
                2, byteorder="big"
            )  # Convert integer tag to byte format
            if tag_bytes in EXIF_TAG_DICT:
                tag_name = EXIF_TAG_DICT[tag_bytes]
                # if tag_name == "MakerNote": break # Just for now
                exif_data[tag_name] = self._parse_tag(
                    data_type=datatype,
                    count=count,
                    value=value,
                    entry_offset=entry_offset,
                    tiff_offset=tiff_header_offset,
                    endianness=endianness,
                    order=i,
                )

        report["EXIF Data"] = exif_data
        return report

    def _parse_tag(
        self, data_type, count, value, entry_offset, tiff_offset, endianness, order
    ) -> dict:
        dt = TAG_TYPES.get(data_type, 7)  # Fetches type UNDEFINED if fails

        if dt in OVERFLOW_TYPES or count > 4:
            content_bytes = self._APP1_SEGMENT[
                value + tiff_offset : value + count + tiff_offset
            ]
            content_offset = value
            if dt in OVERFLOW_TYPES:
                content_bytes = self._APP1_SEGMENT[
                    value + tiff_offset : value + tiff_offset + 8
                ]
                value, decimal_value = self._parse_rational(content_bytes, endianness)
                # value = f"{num}/{denom}" if denom != 1 else num

            return {
                "Markup": f"[{entry_offset}:{entry_offset+12}]",
                "Absolute Offset": entry_offset,
                "TIFF offset": entry_offset - tiff_offset,
                "Recorded Type": data_type,
                "Type": dt,
                "Count": count,
                "Content Location": content_offset,
                "Content": bytes(content_bytes),
                "Content Value": value,
                "Tag Order": order,
                "Status": None,  # Advanced setting, in development
            }

        return {
            "Markup": f"[{entry_offset}:{entry_offset+12}]",
            "Absolute Offset": entry_offset,
            "TIFF offset": entry_offset - tiff_offset,
            "Recorded Type": data_type,
            "Type": dt,
            "Count": count,
            "Content": hex(value),
            "Content Value": value,
            "Tag Order": order,
            "Status": None,  # Advanced setting, in development
        }

    def _parse_rational(
        self, content_bytes, endianness
    ):  # "<" for little-endian, ">" for big-endian
        num, denom = struct.unpack(f"{endianness}II", content_bytes)
        fraction_str = (
            f"{num}/{denom}" if denom else f"{num}/1"
        )  # Avoid division by zero
        decimal_value = num / denom if denom else num  # Compute decimal representation
        return fraction_str, decimal_value  # Return both representations

    def get_image_data(self, verbose: str = None) -> dict:
        """
        Generates a thorough metadata report, including general image information.

        Args:
            verbose (str): Verbosity mode. Options:
                - "exif": Returns only EXIF metadata.

        Returns:
            dict: The metadata report based on the selected verbosity mode.
        """

        # Extract JPEG markers
        jpeg_marker_info = self._read_jpeg_markers()

        if "APP1" not in jpeg_marker_info:
            return {"error": "No APP1 segment found in the image."}

        # Extract APP1 segment and EXIF data
        app1_info = self._read_app1_segment(jpeg_marker_info["APP1"]["offset"][0])
        exif_data = app1_info.get("EXIF Info", {})

        if verbose == "exif":
            return {
                "file_name": self.img_path,
                "exif_data": exif_data,
            }  # Return only EXIF data

        # Construct full report
        _, file_ext = os.path.splitext(self.img_path)
        file_size = len(self.binary_repr)

        return {
            "General File Info": {
                "file_name": self.img_path,
                "file_format": file_ext,
                "file_size_bytes": f"{file_size} bytes",
                "file_size_kbytes": f"{round(file_size/1024, 2)} kbs",
            },
            "jpeg_markers": jpeg_marker_info,
            "APP1 Info": app1_info,
        }

    @classmethod
    def get_image_datas(cls, folder_path: str, verbose: str = None) -> list[dict]:
        """
        Generates metadata reports for all images in a folder.

        Args:
            folder_path (str): Path to the folder containing images.
            verbose (str, optional): Verbosity mode. Options:
                - None (default): Full metadata.
                - "exif": Returns only EXIF metadata.

        Returns:
            list[dict]: List of metadata reports, each corresponding to an image.
        """

        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path.")

        # Get all JPEG images
        image_files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith((".jpg", ".jpeg"))
        ]

        if not image_files:
            raise ValueError("No valid images found in the folder.")

        # Generate reports
        return [cls(img).get_image_data(verbose=verbose) for img in image_files]

    @classmethod
    def metadata_comparison(
        cls, folder_path: str = None, list_of_images: list = None
    ) -> dict:
        """
        Extracts and compares EXIF metadata from multiple images, using the first image as a pivot.

        Args:
            folder_path (str): Path to a folder containing JPEG images.

        Returns:
            dict: Dictionary containing ordered EXIF data across images.
        """
        if not folder_path and not list_of_images:
            raise ValueError("Either folder_path or list_of_images must be provided.")

        if not os.path.isdir(folder_path) and not list_of_images:
            raise ValueError("Invalid folder path.")

        if folder_path:
            image_reports = cls.get_image_datas(folder_path)
        else:
            if not all(isinstance(img, ImageHat) for img in list_of_images):
                raise ValueError(
                    "All elements in list_of_images must be instances of ImageHat."
                )
            image_reports = [
                cls._get_image_data(verbose="exif") for img in list_of_images
            ]

        # Ensure we have enough images for comparison
        if len(image_reports) < 2:
            raise ValueError(
                "At least two images are required for metadata comparison."
            )

        #     # Get only JPEG images
        #     image_files = [
        #         os.path.join(folder_path, f)
        #         for f in os.listdir(folder_path)
        #         if f.lower().endswith((".jpg", ".jpeg"))
        #     ]

        #     if len(image_files) < 2:
        #         raise ValueError("At least two images are required for comparison.")

        # # Generate reports for all images
        #     image_reports = [ImageHat(img).generate_report() for img in image_files]

        # Extract EXIF metadata from reports (first image as pivot)
        pivot_metadata = (
            image_reports[0]
            .get("APP1 Info", {})
            .get("EXIF Info", {})
            .get("EXIF Data", {})
        )
        if not pivot_metadata:
            raise ValueError("No EXIF metadata found in the first image.")

        metadata_records = {tag: [] for tag in pivot_metadata.keys()}

        # Iterate over images and match order with pivot
        for report in image_reports:
            exif_data = (
                report.get("APP1 Info", {}).get("EXIF Info", {}).get("EXIF Data", {})
            )
            for tag in metadata_records:
                metadata_records[tag].append(
                    exif_data.get(tag, None)
                )  # Use None if tag is missing

        return metadata_records


if __name__ == "__main__":

    # NOTE Use the below lines to test
    # file_path_img = r"tests\testsets\testset-small\Sony_DSC_H50_Sony_DSC-H50_0_47713.JPG"
    # img = ImageHat(file_path_img)
    # meta = img_get_image_data()
    # print(meta)
    # print(meta["APP1 Info"]["EXIF Info"]["EXIF DATA"])

    # # NOTE: Testing on all camera models in Dresden Dataset
    testset_folder = os.path.join("tests", "testsets", "testset-small")
    list_of_images = [
        os.path.join(testset_folder, fp) for fp in os.listdir(testset_folder)
    ]
    images = [ImageHat(img) for img in list_of_images]


    for i in images[:4]:
        print(i.get_image_data(verbose="exif"))

    # comp = ImageHat.metadata_comparison(testset_folder)
    # comp = comp.get("FocalLength")
    # for items in comp:
    #     print(items, sep=" ")
