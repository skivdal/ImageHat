# Information of all the applied markers segments found in .JPEG


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

EXIF_IDENTIFIER = b"\x45\x78\x69\x66\x00\x00"

EXIF_DATA = {}




