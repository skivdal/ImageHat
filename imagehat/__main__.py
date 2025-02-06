import os, os.path
import io, struct 
from constants import *
from tag_support_levels import *
from valid_formats import VALID_FORMATS
from output_structure import OUTPUT_STRUCTURE

class ImageHat():

    def __init__(self, img_path):
        self.img_path = img_path # stores the image adress / path
        self.validate_file_path() # validates file path
        self.binary_repr = self.get_binary_data() # creates hexadecimal representaion

    def get_binary_data(self) -> bytes:
        try:
            with open(self.img_path, "rb") as binary_repr:
                binary_content = binary_repr.read()
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

    def validate_exif(self) :
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

    def help(self) -> None:
        """
        A method 
        """
        print("""
        ImageHat Class:
        - Load and analyze binary image files for metadata.
        - Supported Methods:
            - verify_type_image: Checks for valid EXIF or TIFF metadata structure.
            - extract_tags: Extract specific tags and their values from the image.
            - summarize_metadata: Prints a summary of extracted metadata.
        """)

    def read_app1_segment(self, app1_offset):
        """
        This method locates the APP1 segment in the binary image data and return its offset and size.
        """
        report = {}

        # Recording APP1 segment size (2 bytes, \xFF\xE1)
        app1_size = ImageHat.hex_to_decimal(self.binary_repr[app1_offset+2:app1_offset+4]) # Size of APP1 segment in bytes
        report["app1_size"] = app1_size # For latter, add failsafe if segment > 64 kb

        # Recording start of APP1 segment
        app1_location_start = self.binary_repr[app1_offset] 
        report["start_of_app1"] = app1_location_start

        # Recording end of APP1 segment
        app1_location_end = self.binary_repr[app1_offset+app1_size]
        report["end_of_app1"] = app1_location_end

        # Recording EXIF identifier (6 bytes) 
        exif_identifier = self.binary_repr.find(IDENTIFIERS["exif_identifier"])
        report["exif_identifier_loc"] = exif_identifier

        # Recording byte order (2 bytes)
        byte_order_loc = exif_identifier+6
        byte_order = self.binary_repr[byte_order_loc:byte_order_loc+2]
        endianness = "<" if byte_order == IDENTIFIERS["II"] else ">"
        endianness_report = "II" if byte_order == IDENTIFIERS["II"] else "MM"
        report["byte_order"] = endianness_report

        # Recording magic number (2 bytes)
        magic_number_loc = byte_order_loc+2
        magic_number_bytes = self.binary_repr[magic_number_loc:magic_number_loc + 2]  # Read raw bytes
        magic_number = struct.unpack(f"{endianness}H", magic_number_bytes)[0]
        report["tiff_magic_number"] = magic_number_bytes

        ### Extremely important NOTE. All markers and tags in the JEITA documentations are displayed in MSB.
        ### Always unpack constants in big endian from project files. 
        comp_magic_number = struct.unpack(">H", IDENTIFIERS["tiff_magic_number"])[0]
        if  magic_number != comp_magic_number:
            report["tiff_valid"] = False
        else: 
            report["tiff_valid"] = True

        # Extracting offset to first IDF (4 bytes)

        return report, endianness
    
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
            app1_info, endianness = self.read_app1_segment(jpeg_marker_info["APP1"]["offset"][0])
            report["app1_info"] = {
                "app1_size": app1_info["app1_size"],
                "app1_start": app1_info["start_of_app1"],
                "app1_end": app1_info["end_of_app1"],
                "exif_identifier_loc": app1_info["exif_identifier_loc"],
                "byte_order": app1_info["byte_order"],
                "tiff_magic_number": app1_info["tiff_magic_number"],
                "tiff_valid": app1_info["tiff_valid"]
            }
        else:
            return "No APP1 segment found in the image."        
            

        for k,v in report.items():
            print(k, ":" ,v)
            print()
        print(endianness)
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
        Convert a byte sequence (e.g., b'\\xff\\xe1') to a decimal integer.

        Args:
            byte_sequence (bytes): The input byte sequence.
            byteorder (str): JPEG markers are always big endian due to network protocols in accordance with JFIF (APP0). 
            
        Returns:
            int: The decimal representation of the hex value.
        """
        return int.from_bytes(byte_sequence, byteorder=byteorder)
    
    def generate_report_test(self, file_location="reports", file_name="image_report.txt"):
        if not os.path.exists(file_location):
            os.makedirs(file_location, exist_ok=True)
        
        report_path = os.path.join(file_location, file_name)
        with open(report_path, "w", encoding="utf-8") as report_file:
            pass
            # Step 1: Extract JPEG marker segments

            # Step 2: Extract APP1 EXIF marker segment

            # Step 3: Extract TIFF tags


if __name__ == "__main__":
    file_path = r"dataset\archive\Dresden_Exp\Sony_DSC_W170\Sony_DSC-W170_0_50879.JPG"
    img = ImageHat(file_path)
    img.generate_report()
    print(img.binary_repr[:30])


    # for marker,info in img.binary_repr.items():
    #     print(f"Marker {marker} found {info['count']} times at offset: {info['offset']}")
    # print("\n\n\n")




    # img = img.binary_repr[:100]

    # ei = img.find(IDENTIFIERS["exif_identifier"])
    # locs = img[ei:ei+2+6]
    # print(ei, locs, "\n\n\n")
    # app1 = img.find(MARKER_SEGMENTS_JPEG_NAME["APP1"])
    # app1s = img[app1+2:app1+4]
    # print(ImageHat.hex_to_decimal(app1s))

