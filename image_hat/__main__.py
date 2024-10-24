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
                print("This is file contains valid EXIF- or TIFF-structured metadata")
        except Exception as e:
            raise ValueError(f"Binary image data is corrupted: {e}. Are you sure this is a valid file?")


    def get_header(self):

        marker_list = []
        img_data = self.binary_image
        index = 0

        #while in 





    def __str__(self):
        inp = str(input("Are you sure you want a binary string representation of the image?\nThis may be a bad idea.\n"
                    "Press yes or no [y/n]: "))
        match inp:
            case "y":
                print(self.binary_image)
            case "n":
                pass




#file_path = r"C:\Users\saete\OneDrive\Skrivebord\image_hat\images_raise-1k\r000da54ft.NEF" # Replace with the actual path to your .NEF file
file_path = r"data/imgs/IMG_4305.HEIC"
raw = ImageHat(file_path)
# print(raw.img_path)
# print(ImageHat.known_markers)
# raw.verify_type_image()

for seg, name in MARKER_SEGMENTS_JPEG.items():
    if seg in raw.binary_image:
        print(name,":\t",raw.binary_image.find(seg))


print("total lenght of image file", len(raw.binary_image))

if b"\xFF\xE1" in raw.binary_image:
    app1_start = raw.binary_image.find(b"\xff\xe1") # binary loc of APP1 segment
    print("APP1_start", app1_start)

    # size_app1_hex = raw.binary_image[app1_start+2:app1_start+4]
    # dec_value = int.from_bytes(size_app1_hex)
    # app1_end = app1_start + dec_value
    # print(size_app1_hex)
    # print(dec_value)    


if b"\x49\x49" in raw.binary_image:
    print(raw.binary_image.find(b"\x49\x49"))

# def hex_to_ascii(hex_string):
#     return bytes.fromhex(hex_string).decode('utf-8')

# m = hex_to_ascii("49 49 00 2A 00 00 00 08")
# print(m)

# if b"\x01\x10" in raw.binary_image:
#     print("HEYYYYY")
#     val = raw.binary_image.find(b"\x01\x10")
#     out = raw.binary_image[val:val+8]
#     out = str(out)
#     print("THIS", hex_to_ascii(out))




# print(type(binary_image))
# #print(binary_image)
# if b'\xFF\xD8' in binary_image:
#     print("JPEG file detected!")
# else: 
#     print("Not a JPEG file.")

# if b"\xFF\xC0" in binary_image:
#     print("JPEG SOI (start-of-image) found")

print ("\n\n\n")
from PIL import Image
from PIL.ExifTags import TAGS
 
# open the image
image = Image.open("img.jpg")
 
# extracting the exif metadata
exifdata = image.getexif()
 
# looping through all the tags present in exifdata
for tagid in exifdata:
     
    # getting the tag name instead of tag id
    tagname = TAGS.get(tagid, tagid)
 
    # passing the tagid to get its respective value
    value = exifdata.get(tagid)
   
    # printing the final result
    print(f"{tagname:25}: {value}")