# Information of all the applied markers segments found in .JPEG
# NOTE: Both of these dicts are used. They are used in different situations and for testing.

MARKER_SEGMENTS_JPEG_NAME = {
    "SOI" : b"\xFF\xD8", # (Start of Image)
    "APP0" : b"\xFF\xE0", # (JFIF Application Marker)
    "APP1" : b"\xFF\xE1", # (EXIF Application Marker)
    "DQT" : b"\xFF\xDB", # (Define Quantization Table)
    "DHT" : b"\xFF\xC4", # (Define Huffman Table)
    "DRI" : b"\xFF\xDD", # (Restart Interval)
    "SOF0" : b"\xFF\xC0", # (Start of Frame | Baseline DCT)
    "SOF1" : b"\xFF\xC1", # (Start of Frame | Extended Sequential DCT)
    "SOF2" : b"\xFF\xC2", # (Start of Frame | Progressive DCT)
    "SOF3" : b"\xFF\xC3", # (Start of Frame | Lossless JPEG)
    "SOS" : b"\xFF\xDA", # (Scan Header)
    "EOI" : b"\xFF\xD9" # (End of Image)
}

MARKER_SEGMENTS_JPEG_ADDRESS = {
    b"\xFF\xD8": "SOI",  # (Start of Image)
    b"\xFF\xE0": "APP0",  # (JFIF Application Marker)
    b"\xFF\xE1": "APP1",  # (EXIF Application Marker)
    b"\xFF\xDB": "DQT",  # (Define Quantization Table)
    b"\xFF\xC4": "DHT",  # (Define Huffman Table)
    b"\xFF\xDD": "DRI",  # (Restart Interval)
    b"\xFF\xC0": "SOF0",  # (Start of Frame | Baseline DCT)
    b"\xFF\xC1": "SOF1",  # (Start of Frame | Extended Sequential DCT)
    b"\xFF\xC2": "SOF2",  # (Start of Frame | Progressive DCT)
    b"\xFF\xC3": "SOF3",  # (Start of Frame | Lossless JPEG)
    b"\xFF\xDA": "SOS",  # (Scan Header)
    b"\xFF\xD9": "EOI"   # (End of Image)
}

#
IDENTIFIERS = {
    "full_exif_identifier": b"\x45\x78\x69\x66\x00\x00", # "Exif\0\0", including the following NULL value and padding
    "exif_identifier": b"\x45\x78\x69\x66", # HEX representation of EXIF in ASCII
    "II": b"\x49\x49", # Intel byte order, LSB first
    "MM": b"\x4D\x4D", # Motorola byte order, MSB first
    "tiff_magic_number": b"\x00\x2A", # TIFF magic number verifies TIFF
    "offset_first_ifd": b"\x08\x00\x00\x00"	
}




