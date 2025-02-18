
from constants import (MARKER_SEGMENTS_JPEG_ADDRESS,
                       MARKER_SEGMENTS_JPEG_NAME,
                       IDENTIFIERS)
from tag_support_levels import (TAG_TYPES,
                                OVERFLOW_TYPES,
                                TAG_TYPE_SIZE_BYTES,
                                EXIF_TAG_DICT,
                                EXIF_GPS_TAGS_DICT)
from valid_formats import VALID_FORMATS
# from output_structure import (_EXIF_DATA_OUTPUT_4B,
#                               _EXIF_DATA_OUTPUT_L4B)
import os, os.path, struct
from typing import Union

class ImageHat():

    def __init__(self, img_path):
        self.img_path: str = img_path # stores the image adress / path
        self.validate_file_path() # validates file path
        self.binary_repr: bytes = self.get_binary_data() # creates hexadecimal representaion
        self.binary_repr: bytes = self.binary_repr
        self.file_info: Union[None, dict] = None
        self.app1_info: Union[None, dict] = None
        self.exif_info: Union[None, dict] = None

    def get_binary_data(self) -> bytes:
        try:
            with open(self.img_path, "rb") as binary_repr:
                binary_content: bytes = binary_repr.read()
                if not isinstance(binary_content, bytes):
                    binary_content = binary_content.tobytes()
                return binary_content
        except Exception as e:
            print(f"An error occurred: {e}")


    def validate_file_path(self) -> None:
        """
        This method is used for validating the file paths, reducing the chance of error during initializing.
        """
        if not isinstance(self.img_path, str):
            raise TypeError("Not valid type, must be string.")

        if not os.path.exists(self.img_path):
            raise FileNotFoundError(f"The file '{self.img_path}' does not exist or is located elsewhere.")

        _, ext = os.path.splitext(self.img_path)
        if ext.upper() not in VALID_FORMATS:
            raise ValueError(f"Invalid file type '{ext}'. Supported types: {', \n'.join(VALID_FORMATS)}.")

    def validate_exif(self) -> None:
        """
        This method is for verifying that
        """
        if not MARKER_SEGMENTS_JPEG_NAME["APP1"] in self.binary_repr:
            raise ValueError(f"Binary image does not contain Application Layer 1. No EXIF data found.")

        if not IDENTIFIERS["IDENTIFIERS"] in self.binary_repr:
            raise ValueError(f"Binary image does not contain an EXIF identifier.")

    def __str__(self) -> str:
        return f"ImageHat: {self.img_path}, Size: {len(self.binary_repr)} bytes"

    def show_data(self) -> None:
        """
        Metod for printing the whole byte array. Should be avoided as printed byte arrays are living nightmares.
        """
        print(self.binary_repr)

    @staticmethod
    def help(self) -> None:
        """
        Displays information about the ImageHat class and its available methods.

        The ImageHat class is designed to analyze binary image files, extract metadata,
        and validate EXIF structures. It supports methods for reading JPEG markers,
        parsing EXIF data, and converting hex values.

        Available Methods:
        ------------------

        - show_data():
            Prints extracted metadata in a human-readable format.

        - validate_exif():
            Checks if the image contains a valid EXIF structure.
            Returns True if valid, otherwise False.

        - validate_file_path():
            Validates whether the provided file path exists and is accessible.
            Raises an error if the path is invalid.

        - get_binary_data() -> bytes:
            Reads the image file in binary mode and returns the raw data.

        - read_app1_segment(app1_offset):
            Reads the APP1 (EXIF) segment from the JPEG file at the given offset.
            Returns parsed EXIF data if present.

        - read_exif_ifd(ifd_start, num_entries, tiff_header_offset, endianness):
            Reads and extracts metadata from an EXIF Image File Directory (IFD).
            Returns a dictionary of parsed EXIF tags.

        - generate_report():
            Compiles and returns a detailed report of extracted metadata.

        - read_jpeg_markers() -> dict:
            Identifies and extracts key JPEG markers (e.g., SOI, APP1, DQT, SOS).
            Returns a dictionary mapping marker names to their offsets.

        - hex_to_decimal(byte_sequence: bytes, byteorder: str = 'big') -> int:
            Converts a byte sequence into an integer.
            Supports 'big' and 'little' endian formats.
            Returns the decimal representation of the byte sequence.

        Example Usage:
        --------------
        >>> image = ImageHat("sample.jpg")
        >>> image.validate_exif()
        True
        >>> binary_data = image.get_binary_data()
        >>> print(binary_data[:10])  # Print first 10 bytes of the file
        >>> markers = image.read_jpeg_markers()
        >>> print(markers)
        {'SOI': 0, 'APP1': 20, 'DQT': 100, 'SOS': 200}

        """

        print("""
        ImageHat Class:
        ----------------
        A class for analyzing binary image files and extracting metadata.

        Supported Methods:
        - show_data(): Displays extracted metadata in a readable format.
        - validate_exif(): Checks for a valid EXIF structure.
        - validate_file_path(): Verifies if the provided file path exists.
        - get_binary_data(): Reads the image file and returns raw binary data.
        - read_app1_segment(app1_offset): Reads and parses the APP1 (EXIF) segment.
        - read_exif_ifd(ifd_start, num_entries, tiff_header_offset, endianness): Extracts EXIF IFD metadata.
        - generate_report(): Generates a detailed metadata report.
        - read_jpeg_markers(): Extracts key JPEG markers and their positions.
        - hex_to_decimal(byte_sequence, byteorder): Converts a byte sequence to an integer.

        Example:
        --------
        image = ImageHat("sample.jpg")
        image.validate_exif()
        binary_data = image.get_binary_data()
        markers = image.read_jpeg_markers()
        print(markers)
        """)



    def read_app1_segment(self, app1_offset) -> dict:
        """
        This method locates the APP1 segment in the binary image data and return its offset and size.
        """
        report = {}

        # Recording APP1 segment size (2 bytes, \xFF\xE1)
        app1_size = ImageHat.hex_to_decimal(self.binary_repr[app1_offset+2:app1_offset+4]) # Size of APP1 segment in bytes
        report["APP1 Size"] = app1_size # For latter, add failsafe if segment > 64 kb

        # Recording start of APP1 segment
        app1_location_start = self.binary_repr[app1_offset]
        report["Start of APP1"] = app1_location_start

        # Recording end of APP1 segment
        app1_location_end = self.binary_repr[app1_offset+app1_size]
        report["End of APP1"] = app1_location_end
        _0_TO_APP1 = self.binary_repr[:app1_location_end]

        # Recording EXIF identifier (6 bytes)
        exif_identifier = _0_TO_APP1.find(IDENTIFIERS["exif_identifier"])
        report["EXIF Identifier Offset"] = exif_identifier

        # Recording byte order (2 bytes)
        # Recoring endianness starts here. EXIF is big-endian until byte-order is discovered.
        byte_order_offset = exif_identifier+6
        byte_order_bytes = _0_TO_APP1[byte_order_offset:byte_order_offset+2]
        endianness = "<" if byte_order_bytes == IDENTIFIERS["II"] else ">"
        endianness_report = "II" if byte_order_bytes == IDENTIFIERS["II"] else "MM"
        report["Byte Order"] = endianness_report

        # Recording magic number (2 bytes)
        magic_number_offset = byte_order_offset+2
        magic_number_bytes = _0_TO_APP1[magic_number_offset:magic_number_offset + 2]  # Read raw bytes
        magic_number = struct.unpack(f"{endianness}H", magic_number_bytes)[0]
        report["TIFF Magic Number"] = magic_number_bytes
        report["TIFF Magic Number Offset"] = magic_number_offset

        ### Extremely important NOTE. All markers and tags in the JEITA documentations are displayed in MSB.
        ### Always unpack constants in big endian from project files.
        comp_magic_number = struct.unpack(">H", IDENTIFIERS["tiff_magic_number"])[0]
        report["TIFF Validity"] = magic_number == comp_magic_number

        # Recording offset to first IDF (4 bytes)
        ifd_offset_bytes = _0_TO_APP1[byte_order_offset+4:byte_order_offset+8]
        ifd_start = byte_order_offset + struct.unpack(f"{endianness}I", ifd_offset_bytes)[0]
        ifd_entries = struct.unpack(f"{endianness}H", _0_TO_APP1[ifd_start:ifd_start+2])[0]
        report["0th IFD"] = ifd_offset_bytes
        report["0th IFD start"] = ifd_start
        report["Entries in 0th IFD"] = ifd_entries


        # Recording the EXIF tags. NOTE: Most important, do not touch.
        exif_information = self.read_exif_ifd(ifd_start=ifd_start,
                                              num_entries=ifd_entries,
                                              tiff_header_offset=byte_order_offset,
                                              endianness=endianness)
        report["EXIF Information"] = exif_information


        return report

    def read_exif_ifd(self, ifd_start, num_entries, tiff_header_offset, endianness) -> dict:
        """
        Reads and extracts all Exif IFD entries.
        """
        report = {}

        # This loop starts at the recorded start of the first ifd,
        # skips the 2 num_entries bytes, and iterates over each entry.
        exif_ifd_offset = None
        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry*12)
            tag, datatype, count, value_offset = struct.unpack(f"{endianness}HHII", self.binary_repr[entry_offset:entry_offset+12])
            if tag == 0x8769:  # Exif IFD Pointer
                exif_ifd_offset = tiff_header_offset + value_offset
                report["Exif IFD pointer found"] = bool(tag)
                break

        if not exif_ifd_offset:
            return "Exif IFD Pointer not found"

        # Read number of entries in Exif IFD
        num_exif_entries = struct.unpack(f"{endianness}H", self.binary_repr[exif_ifd_offset:exif_ifd_offset + 2])[0]
        report["Number of Exif Entries"] = num_exif_entries

        # Extract key EXIF tags
        exif_data = {}

        # Iterate over the Exif specific IFD entries
        for i in range(num_exif_entries):
            entry_offset = exif_ifd_offset + 2 + (i * 12) # Rec
            tag, data_type, count, value = struct.unpack(f"{endianness}HHII", self.binary_repr[entry_offset:entry_offset+12])


            tag_bytes = tag.to_bytes(2, byteorder="big")  # Convert integer tag to byte format
            if tag_bytes in EXIF_TAG_DICT:
                tag_name = EXIF_TAG_DICT[tag_bytes]
                if tag_name == "MakerNote": break # Just for now
                exif_data[tag_name] = self.parse_tag(data_type=data_type,
                                                     count=count,
                                                     value=value,
                                                     entry_offset=entry_offset,
                                                     tiff_offset=tiff_header_offset,
                                                     endianness=endianness)

        report["exif_data"] = exif_data
        return report

    def parse_tag(self, data_type, count, value, entry_offset, tiff_offset, endianness) -> dict:
        dt = TAG_TYPES.get(data_type, 7) # Fetches type UNDEFINED if fails

        if dt in OVERFLOW_TYPES or count > 4:
            content_bytes = self.binary_repr[value+tiff_offset:value+count+tiff_offset]
            content_offset = value
            if dt in OVERFLOW_TYPES:
                content_bytes = self.binary_repr[value+tiff_offset:value+tiff_offset+8]
                num, denom = struct.unpack(f"{endianness}II", content_bytes)
                value = num/denom

            # content_bytes = self.binary_repr[value+tiff_offset:value+count+tiff_offset]
            # # content = struct.unpack(f"{endianness}", content_bytes)[0]
            return {
                "Markup": f"[{entry_offset}:{entry_offset+12}]",
                "Absolute Offset":entry_offset,
                "TIFF offset":entry_offset-tiff_offset,
                "Recorded Type": data_type,
                "Type": dt,
                "Count": count,
                "Content Location": content_offset,
                "Content": bytes(content_bytes),
                "Content Value": value,
                "Status":None # Advanced setting, in development
            }

        return {
            "Markup": f"[{entry_offset}:{entry_offset+12}]",
            "Absolute Offset": entry_offset,
            "TIFF offset": entry_offset-tiff_offset,
            "Recorded Type":data_type,
            "Type": dt,
            "Count": count,
            "Content": hex(value),
            "Content Value": value,
            "Status":None # Advanced setting, in development
        }
    


        

    def generate_report(self):
        """
        Generates a thorough metadata report.

        Returns:
            dict: Report of markers, APP1 data, TIFF tags, and metadata.
        """
        report = {}

        ### NOTE Step 1: General file data
        _, file_ext = os.path.splitext(self.img_path)
        file_size = len(self.binary_repr)
        report["general_file_info"] = {
            "file_name":self.img_path,
            "file_format":file_ext,
            "file_size_bytes":f"{file_size} bytes",
            "file_size_kbytes":f"{round(file_size/1024, 2)} kbs"
        }

        jpeg_marker_info = self.read_jpeg_markers()
        report["jpeg_markers"] = jpeg_marker_info

        if jpeg_marker_info["APP1"]:
            app1_info = self.read_app1_segment(jpeg_marker_info["APP1"]["offset"][0])
            report["app1_info"] = app1_info
        else:
            return "No APP1 segment found in the image."

        self.file_info = report["general_file_info"]
        self.app1_info = {k: v for k, v in report["app1_info"].items() if k != "EXIF Information"}
        self.exif_info = report["app1_info"]["EXIF Information"]
  
        return report

    def read_jpeg_markers(self) -> dict:
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
                marker_info[name] = {
                    "count": len(offset),
                    "offset": offset
                }

        return marker_info

    @classmethod
    def hex_to_decimal(cls, byte_sequence: bytes, byteorder: str = 'big') -> int:
        """
        Convert a b3yte sequence (e.g., b'\\xff\\xe1') to a decimal integer.

        Args:
            byte_sequence (bytes): The input byte sequence.
            byteorder (str): JPEG markers are always big endian due to network protocols in accordance with JFIF (APP0).

        Returns:
            int: The decimal representation of the hex value.
        """
        return int.from_bytes(byte_sequence, byteorder=byteorder)

    def generate_report_test(self, file_location="reports", file_name="image_report.txt") -> None:
        if not os.path.exists(file_location):
            os.makedirs(file_location, exist_ok=True)

        report_path = os.path.join(file_location, file_name)
        with open(report_path, "w", encoding="utf-8") as report_file:
            pass
            # Step 1: Extract JPEG marker segments

            # Step 2: Extract APP1 EXIF marker segment

            # Step 3: Extract TIFF tags


if __name__ == "__main__":
    # file_path = r"dataset\archive\Dresden_Exp\Sony_DSC_W170\Sony_DSC-W170_0_50879.JPG"
    file_path = r"tests\testsets\testset-small\Sony_DSC_H50_Sony_DSC-H50_0_47713.JPG"
    img = ImageHat(file_path)
    report = img.generate_report()
    print

    # testset_folder = r"tests\testsets\testset-small"
    # list_of_images = [os.path.join(testset_folder, fp) for fp in os.listdir(testset_folder)]
    # images = [ImageHat(img) for img in list_of_images]
    
    # for img in images[:10]:
    #     report = img.generate_report()
    #     try:
    #         print(report["app1_info"]["EXIF Information"]["exif_data"])
    #         print("\n\n\n\n")
    #     except:
    #         pass
    for k,v in report["app1_info"]["EXIF Information"]["exif_data"].items():
        print(f"{k}: {v}")
        print()

    print(img.app1_info)