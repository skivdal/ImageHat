import os, os.path, tkinter
from jpeg_marker_information import MARKER_SEGMENTS_JPEG
from valid_formats import VALID_FORMATS
from tag_support_levels import *
import pandas as pd
import io, struct 

class ImageHat():

    def __init__(self, img_path):
        if not isinstance(img_path, str):
            raise TypeError("Not valid type, must be string.")
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"The file '{img_path}' does not exist.")
        
        _, ext = os.path.splitext(img_path)
        if ext.upper() not in VALID_FORMATS:
            raise ValueError(f"Invalid file type '{ext}'. Supported types: {', \n'.join(VALID_FORMATS)}.")
        
        self.img_path = img_path # stores the image adress / path
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

    

    

    def verify_type_image(self):
        try:
            if b"\xFF\xD8" in self.binary_image and b"\xFF\xC0" in self.binary_image:
                print("This file contains valid EXIF- or TIFF-structured metadata")
        except Exception as e:
            raise ValueError(f"Binary image data is corrupted: {e}.\n\n Are you sure this is a valid file?")


    def find_exif_bytes(self, pattern=b"    0"):
        """
        Searches for a specific EXIF byte pattern in the binary image data.
        """
        if pattern in self.binary_image:
            location = self.binary_image.find(pattern)
            return f"EXIF bytes found at: {location}"
        else:
            return ("EXIF bytes not found.")
    





    def __str__(self):
        inp = str(input("Are you sure you want a binary string representation of the image?\nThis may be a bad idea.\n"
                    "Press yes or no [y/n]: "))
        match inp:
            case "y":
                print(self.binary_image)
            case "n":
                pass





#file_path = r"data\imgs\r012d1dbet.NEF" 
file_path = r"data/imgs/IMG_4304.HEIC"
#file_path = r"C:\Users\saete\OneDrive\Skrivebord\archive\data\dogs\dog.2.jpg"
raw = ImageHat(file_path)
# print(raw.img_path)
# print(ImageHat.known_markers)
# raw.verify_type_image()

#ex = dict(list(TIFF_SPECIFIC_ATTRIBS.items())[:10])
ex = dict(list(EXIF_IFD_ATTRIB_INFO_1.items())[:10])
print(ex, "\n")

tag_positions = {}

# Loop through each tag in TIFF_SPECIFIC_ATTRIBS
for tag, properties in ex.items():
    hex_value = properties["Hex"]
    tag_positions[tag] = []
    print(properties)

    # Determine the byte size of the tag data based on its type and count
    data_type = properties["Type"]
    try:
        data_length = TYPE_SIZE_BYTES[data_type]
    except TypeError as e:
        data_length = TYPE_SIZE_BYTES[max(data_type)]

    # Search for all occurrences of the hex value in the binary image data
    start = 0
    while start < len(raw.binary_image):
        pos = raw.binary_image.find(hex_value, start)
        if pos == -1:
            break  # No more occurrences found

        # Append the position and calculate the data following the tag
        data_start = pos + len(hex_value)
        tag_positions[tag].append((pos, raw.binary_image[data_start:data_start + data_length]))
        
        start = pos + len(hex_value)  # Move past this occurrence

# Filter out tags that were not found
tag_positions = {tag: positions for tag, positions in tag_positions.items() if positions}

print("\n\n")
for k,v in tag_positions.items():
    print(k,len(v))


print(raw.binary_image.find(b"\xFF\xE1"))
count = raw.binary_image.count(b"\xFF\xE1") 
print(count)

print(raw.binary_image.find(b"\x45\x78\x69\x66\x00\x00"))
# if b"\xFF\xE1" in raw.binary_image:
#     app1_start = raw.binary_image.find(b"\xff\xe1") # binary loc of APP1 segment
#     print(raw.binary_image[app1_start:app1_start+10])


# def hex_to_ascii(hex_string):
#     return bytes.fromhex(hex_string).decode('utf-8')

# li = []

# # Iterate through the entire binary image, one byte at a time
# for i in range(len(raw.binary_image) - 9):  # Stop 9 bytes before the end to avoid index out of range
#     if raw.binary_image[i:i + 2] == b"EXIF":  # Check for the byte sequence "\x49\x49"
#         li.append(i)  # Append the index where the sequence was found
app1_marker = b"\xFF\xE1"
exif_identifier = b"\x45\x78\x69\x66\x00\x00"

app1_positions = []
start = 0
while start < len(raw.binary_image):
    pos = raw.binary_image.find(app1_marker, start)
    if pos == -1:
        break
    app1_positions.append(pos)
    start = pos + len(app1_marker)

# Find the position of the identifier
identifier_pos = raw.binary_image.find(exif_identifier)

# Determine which APP1 marker comes closest after the identifier
closest_app1_after_identifier = None
for pos in app1_positions:
    if pos > identifier_pos:
        closest_app1_after_identifier = pos
        break  # Stop at the first APP1 marker after the identifier

# Print results
if identifier_pos != -1:
    print(f"Identifier found at position: {identifier_pos}")
else:
    print("Identifier not found.")

if closest_app1_after_identifier:
    print(f"First APP1 marker after identifier is at position: {closest_app1_after_identifier}")
else:
    print("No APP1 marker found after the identifier.")


seg = raw.binary_image.find(app1_marker)
print(raw.binary_image[seg:seg+12])