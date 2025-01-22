import os, os.path
import io, struct 
from constants import MARKER_SEGMENTS_JPEG_NAME, MARKER_SEGMENTS_JPEG_ADDRESS
from valid_formats import VALID_FORMATS
from tag_support_levels import *
from output_structure import DATA_STRUCT


class ImageHat():

    def __init__(self, img_path):
        self.img_path = img_path # stores the image adress / path
        self.validate_file_path()
        self.binary_image = self.get_binary_data()


    def get_binary_data(self):
        try:
            with open(self.img_path, "rb") as binary_image:
                binary_content = binary_image.read()
                if not isinstance(binary_content, bytes):
                    binary_content = binary_content.tobytes()
                return binary_content  
        except Exception as e:
            print(f"An error occurred: {e}")

        
    def validate_file_path(self):
        if not isinstance(self.img_path, str):
            raise TypeError("Not valid type, must be string.")
        
        if not os.path.exists(self.img_path):
            raise FileNotFoundError(f"The file '{self.img_path}' does not exist.")
        
        _, ext = os.path.splitext(self.img_path)
        if ext.upper() not in VALID_FORMATS:
            raise ValueError(f"Invalid file type '{ext}'. Supported types: {', \n'.join(VALID_FORMATS)}.")

    def verify_type_image(self):
        try:
            if MARKER_SEGMENTS_JPEG_NAME["APP0"] in self.binary_image and b"\xFF\xC0" in self.binary_image:
                print("This file contains valid EXIF- or TIFF-structured metadata")
        except Exception as e:
            raise ValueError(f"Binary image data is corrupted: {e}.\n\n Are you sure this is a valid file?")

    def __str__(self):
        return f"ImageHat: {self.img_path}, Size: {len(self.binary_image)} bytes"
    
    def show_data(self):
        print(self.binary_image)

    def help(self):
        print("""
        ImageHat Class:
        - Load and analyze binary image files for metadata.
        - Supported Methods:
            - verify_type_image: Checks for valid EXIF or TIFF metadata structure.
            - extract_tags: Extract specific tags and their values from the image.
            - summarize_metadata: Prints a summary of extracted metadata.
        """)

    def find_app1_segment(self):
        """
        Locate the APP1 segment in the binary image data and return its position and size.
        """
        app1_marker = b"\xFF\xE1"  # APP1 marker
        exif_identifier = b"Exif\x00\x00"  # EXIF identifier string (ASCII)

        # Find all occurrences of the APP1 marker
        app1_positions = self.find_occurrences(app1_marker)

        if not app1_positions:
            return "No APP1 segment found in the image."

        # Check for the EXIF identifier following each APP1 marker
        for pos in app1_positions:
            # Extract the APP1 segment length (next 2 bytes after the marker)
            length_bytes = self.binary_image[pos + 2:pos + 4]
            if len(length_bytes) < 2:
                continue  # Skip invalid APP1 segment

            # Convert the length to an integer (big-endian format)
            segment_length = int.from_bytes(length_bytes, byteorder="big")

            # Check if EXIF identifier exists in the segment
            segment_data = self.binary_image[pos:pos + segment_length]
            if exif_identifier in segment_data:
                return {
                    "start_position": pos,
                    "length": segment_length,
                    "segment_data": segment_data,
                }

        return "APP1 marker(s) found, but no EXIF identifier present."
    
    def find_jpeg_markers(self):
        markers = {
            "SOI": b"\xFF\xD8",
            "APP0": b"\xFF\xE0",
            "APP1": b"\xFF\xE1",
            "DQT": b"\xFF\xDB",
            "SOF0": b"\xFF\xC0",
            "SOS": b"\xFF\xDA",
            "EOI": b"\xFF\xD9",
        }
        found_markers = {}
        for name, marker in markers.items():
            pos = self.binary_image.find(marker)
            if pos != -1:
                found_markers[name] = pos
        return found_markers





#file_path = r"data/imgs/IMG_4304.HEIC"
# file_path = r"excluded_data\archive\Dresden_Exp\Nikon_D70\Nikon_D70_0_19445.JPG"
file_path1 = r"excluded_data\archive\Dresden_Exp\Sony_DSC_W170\Sony_DSC-W170_0_50879.JPG"
raw = ImageHat(file_path1)


markers = raw.find_jpeg_markers()
for name, pos in markers.items():
    print(f"{name} found at offset: {hex(pos)}")



print(raw.binary_image.find(b"\xFF\xE1"))
count = raw.binary_image.count(b"\xFF\xE1") 
print(count)

print(raw.binary_image.find(b"\x45\x78\x69\x66\x00\x00"))

app1_marker = b"\xFF\xE1"
exif_identifier = b"\x45\x78\x69\x66\x00\x00"

# app1_positions = []
# start = 0
# while start < len(raw.binary_image):
#     pos = raw.binary_image.find(app1_marker, start)
#     if pos == -1:
#         break
#     app1_positions.append(pos)
#     start = pos + len(app1_marker)

# # Find the position of the identifier
# identifier_pos = raw.binary_image.find(exif_identifier)

# # Determine which APP1 marker comes closest after the identifier
# closest_app1_after_identifier = None
# for pos in app1_positions:
#     if pos > identifier_pos:
#         closest_app1_after_identifier = pos
#         break  # Stop at the first APP1 marker after the identifier

# seg = raw.binary_image.find(app1_marker)
# print(raw.binary_image[seg:seg+12])

