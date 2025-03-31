# Information of all the applied markers segments found in .JPEG
# NOTE: Both of the twp next dicts are used. They are used in different situations and for testing.
MARKER_SEGMENTS_JPEG_NAME = {
    "SOI": b"\xff\xd8",  # (Start of Image)
    "APP0": b"\xff\xe0",  # (JFIF Application Marker)
    "APP1": b"\xff\xe1",  # (EXIF Application Marker)
    "DQT": b"\xff\xdb",  # (Define Quantization Table)
    "DHT": b"\xff\xc4",  # (Define Huffman Table)
    "DRI": b"\xff\xdd",  # (Restart Interval)
    "SOF0": b"\xff\xc0",  # (Start of Frame | Baseline DCT)
    "SOF1": b"\xff\xc1",  # (Start of Frame | Extended Sequential DCT)
    "SOF2": b"\xff\xc2",  # (Start of Frame | Progressive DCT)
    "SOF3": b"\xff\xc3",  # (Start of Frame | Lossless JPEG)
    "SOS": b"\xff\xda",  # (Scan Header)
    "EOI": b"\xff\xd9",  # (End of Image)
}

MARKER_SEGMENTS_JPEG_ADDRESS = {
    b"\xff\xd8": "SOI",  # (Start of Image)
    b"\xff\xe0": "APP0",  # (JFIF Application Marker)
    b"\xff\xe1": "APP1",  # (EXIF Application Marker)
    b"\xff\xdb": "DQT",  # (Define Quantization Table)
    b"\xff\xc4": "DHT",  # (Define Huffman Table)
    b"\xff\xdd": "DRI",  # (Restart Interval)
    b"\xff\xc0": "SOF0",  # (Start of Frame | Baseline DCT)
    b"\xff\xc1": "SOF1",  # (Start of Frame | Extended Sequential DCT)
    b"\xff\xc2": "SOF2",  # (Start of Frame | Progressive DCT)
    b"\xff\xc3": "SOF3",  # (Start of Frame | Lossless JPEG)
    b"\xff\xda": "SOS",  # (Scan Header)
    b"\xff\xd9": "EOI",  # (End of Image)
}
"""
JPEG_MARKES = {
    0xD8: "SOI",
    0xD9: "EOI",
    0xC0: "SOF0",
    0xC2: "SOF2",
    0xC4: "DHT",
    0xDB: "DQT",
    0xDD: "DRI",
    0xDA: "SOS",
    0xE0: "APP0",
    0xE1: "APP1",
    0xE2: "APP2",
    0xE3: "APP3",
    0xE4: "APP4",
    0xE5: "APP5",
    0xE6: "APP6",
    0xE7: "APP7",
    0xE8: "APP8",
    0xE9: "APP9",
    0xEA: "APP10",
    0xEB: "APP11",
    0xEC: "APP12",
    0xED: "APP13",
    0xEE: "APP14",
    0xEF: "APP15",
    0xFE: "COM"
}
"""

# Dict used for locating important segments of JPEG binary files
IDENTIFIERS = {
    "full_exif_identifier": b"\x45\x78\x69\x66\x00\x00",  # "Exif\0\0", including the following NULL value and padding
    "exif_identifier": b"\x45\x78\x69\x66",  # HEX representation of EXIF in ASCII
    "II": b"\x49\x49",  # Intel byte order, LSB first
    "MM": b"\x4d\x4d",  # Motorola byte order, MSB first
    "tiff_magic_number": b"\x00\x2a",  # TIFF magic number verifies TIFF
    "offset_first_ifd": b"\x00\x00\x00\x08",  # Offset to the start  of the first IFD
    "exif_ifd_pointer": b"\x87\x69",  # The EXIF IFD pointer
    "gps_ifd_pointer": b"\x88\x25",  # The GPS IFD pointer
    "interoperatbility_ifd_pointer": b"\xa0\x05",  # The Interoperability IFD pointer
}

# Used for indentifying character information in byte chuncks that are of type UNDEFINED
CHARACTER_IDENTIFIER_CODES = {
    "ASCII_cc": b"\x41\x53\x43\x49\x49\x00\x00\x00",  # ASCII character code encoding
    "JIS_cc": b"\x4a\x49\x53\x00\x00\x00\x00\x00",  # Japanese character code encoding (we're dealing with a japanese standard)
    "Unicode_cc": b"\x55\x4e\x49\x43\x4f\x44\x45\x00",  # UTF-8, unicode character code encoding
    "undefined_cc": b"\x00\x00\x00\x00\x00\x00\x00\x00",  # No specific character code encoding (any)
}

EXIF_IFDS = {
    "exif_ifd_pointer": b"\x87\x69",
    "gps_ifd_pointer": b"\x88\x25",
    "interoperability_ifd_pointer": b"\xa0\x05",
}
