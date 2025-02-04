import os, os.path
import io, struct 
from imagehat.constants import *
from imagehat.tag_support_levels import *
from imagehat.valid_formats import VALID_FORMATS
from imagehat.output_structure import OUTPUT_STRUCTURE


class ImageHat():

    def __init__(self, img_path):
        self.img_path = img_path # stores the image adress / path
        self.validate_file_path()
        self.binary_image = self.get_binary_data()


    def get_binary_data(self) -> bytes:
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
            raise FileNotFoundError(f"The file '{self.img_path}' does not exist or is located elsewhere.")
        
        _, ext = os.path.splitext(self.img_path)
        if ext.upper() not in VALID_FORMATS:
            raise ValueError(f"Invalid file type '{ext}'. Supported types: {', \n'.join(VALID_FORMATS)}.")

    def verify_type_image(self):
        try:
            if MARKER_SEGMENTS_JPEG_NAME["APP0"] in self.binary_image and b"\xFF\xC0" in self.binary_image:
                print("This file contains valid EXIF- or TIFF-structured metadata")
        except Exception as e:
            raise ValueError(f"Binary image data is corrupted: {e}.\n\n Are you sure this is a valid file?")

    def __str__(self) -> str:
        return f"ImageHat: {self.img_path}, Size: {len(self.binary_image)} bytes"
    
    def show_data(self) -> None:
        print(self.binary_image)

    def help(self) -> None:
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
    
    def find_jpeg_segments(self) -> dict:
        found_markers = {}
        for addr, name in MARKER_SEGMENTS_JPEG_ADDRESS.items():
            pos = self.binary_image.find(addr)
            if pos != -1:
                found_markers[name] = pos
        return found_markers





#file_path = r"data/imgs/IMG_4304.HEIC"
# file_path = r"excluded_data\archive\Dresden_Exp\Nikon_D70\Nikon_D70_0_19445.JPG"
# file_path = r"dataset\archive\Dresden_Exp\Sony_DSC_W170\Sony_DSC-W170_0_50879.JPG"
# raw = ImageHat(file_path)
# print(len(raw.binary_image))

# markers = raw.find_jpeg_segments()
# for name, pos in markers.items():
#     print(f"{name} found at offset: {(pos)}")


# print("APP1 segment marker address: ", raw.binary_image.find(b"\xFF\xE1"))
# count = raw.binary_image.count(b"\xFF\xE1") 
# print("Count of found APP1 markers: ", count)

# exif_id_loc = raw.binary_image.find(EXIF_IDENTIFIER)
# print("Location of exif identifier: ", exif_id_loc)
file_path = r"dataset\archive\Dresden_Exp\Sony_DSC_W170\Sony_DSC-W170_0_50879.JPG"
raw = ImageHat(file_path)

# # Count occurrences of each marker
# marker_counts = {marker.hex(): raw.binary_image.count(marker) for marker in MARKER_SEGMENTS_JPEG_ADDRESS}

# # Print results
# for marker, count in marker_counts.items():
#     print(f"Marker {marker.upper()} found {count} times.")



# Function to find all positions of a given marker
def find_marker_positions(binary_data, marker):
    positions = []
    pos = binary_data.find(marker)  # Find first occurrence
    while pos != -1:
        positions.append(pos)
        pos = binary_data.find(marker, pos + 1)  # Find next occurrence
    return positions

# Dictionary to store counts and positions
marker_info = {}

for name, marker in MARKER_SEGMENTS_JPEG_NAME.items():
    positions = find_marker_positions(raw.binary_image, marker)
    marker_info[name] = {
        "count": len(positions),
        "positions": positions
    }

# Print results
for marker, info in marker_info.items():
    print(f"Marker {marker} found {info['count']} times at positions: {info['positions']}")
