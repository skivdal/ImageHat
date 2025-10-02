import sys
import json
from imagehat.parsers.jpeg_parser import JPEGParser


filename = sys.argv[1]
img = JPEGParser(filename)
data = img.get_exif_image_data()

print(json.dumps(data))