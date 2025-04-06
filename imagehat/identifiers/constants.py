# Information of all the applied markers segments found in .JPEG
# NOTE: Both of the twp next dicts are used. They are used in different situations and for testing.
MARKER_SEGMENTS_JPEG_NAME = {
    # Start/End of Image
    "SOI": b"\xff\xd8",  # (Start of Image)
    "EOI": b"\xff\xd9",  # (End of Image)

    # Application Markers (APPn)
    "APP0": b"\xff\xe0",  # (JFIF Application Marker)
    "APP1": b"\xff\xe1",  # (EXIF Application Marker)
    "APP2": b"\xff\xe2",  # ICC Profile / FlashPix
    "APP3": b"\xff\xe3",
    "APP4": b"\xff\xe4",
    "APP5": b"\xff\xe5",
    "APP6": b"\xff\xe6",
    "APP7": b"\xff\xe7",
    "APP8": b"\xff\xe8",
    "APP9": b"\xff\xe9",
    "APP10": b"\xff\xea",
    "APP11": b"\xff\xeb",
    "APP12": b"\xff\xec",
    "APP13": b"\xff\xed",  # Photoshop IPTC
    "APP14": b"\xff\xee",  # Adobe
    "APP15": b"\xff\xef",

    # Comment
    "COM": b"\xff\xfe",  # Comment

    # Define Markers
    "DQT": b"\xff\xdb",  # (Define Quantization Table)
    "DHT": b"\xff\xc4",  # (Define Huffman Table)
    "DRI": b"\xff\xdd",  # (Restart Interval)

    # Start of Frame Markers
    "SOF0": b"\xff\xc0",  # (Start of Frame | Baseline DCT)
    "SOF1": b"\xff\xc1",  # (Start of Frame | Extended Sequential DCT)
    "SOF2": b"\xff\xc2",  # (Start of Frame | Progressive DCT)
    "SOF3": b"\xff\xc3",  # (Start of Frame | Lossless JPEG)
    "SOS": b"\xff\xda",  # (Scan Header)
}

MARKER_SEGMENTS_JPEG_ADDRESS = {
    # Start/End of Image
    b"\xff\xd8": "SOI",   # (Start of Image)
    b"\xff\xd9": "EOI",   # (End of Image)

    # Application Markers (APPn)
    b"\xff\xe0": "APP0",  # (JFIF Application Marker)
    b"\xff\xe1": "APP1",  # (EXIF Application Marker)
    b"\xff\xe2": "APP2",  # ICC Profile / FlashPix
    b"\xff\xe3": "APP3",
    b"\xff\xe4": "APP4",
    b"\xff\xe5": "APP5",
    b"\xff\xe6": "APP6",
    b"\xff\xe7": "APP7",
    b"\xff\xe8": "APP8",
    b"\xff\xe9": "APP9",
    b"\xff\xea": "APP10",
    b"\xff\xeb": "APP11",
    b"\xff\xec": "APP12",
    b"\xff\xed": "APP13",  # Photoshop IPTC
    b"\xff\xee": "APP14",  # Adobe
    b"\xff\xef": "APP15",

    # Comment
    b"\xff\xfe": "COM",    # (Comment)

    # Define Markers
    b"\xff\xdb": "DQT",    # (Define Quantization Table)
    b"\xff\xc4": "DHT",    # (Define Huffman Table)
    b"\xff\xdd": "DRI",    # (Restart Interval)

    # Start of Frame Markers
    b"\xff\xc0": "SOF0",   # (Start of Frame | Baseline DCT)
    b"\xff\xc1": "SOF1",   # (Start of Frame | Extended Sequential DCT)
    b"\xff\xc2": "SOF2",   # (Start of Frame | Progressive DCT)
    b"\xff\xc3": "SOF3",   # (Start of Frame | Lossless JPEG)

    # Scan Header
    b"\xff\xda": "SOS",    # (Scan Header)
}


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
