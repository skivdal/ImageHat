# Information of all the applied markers segments found in .JPEG
# NOTE: Both of the two next dicts are used. They are used in different situations and for testing.
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
    # Restart Markers
    "RST0": b"\xff\xd0",
    "RST1": b"\xff\xd1",
    "RST2": b"\xff\xd2",
    "RST3": b"\xff\xd3",
    "RST4": b"\xff\xd4",
    "RST5": b"\xff\xd5",
    "RST6": b"\xff\xd6",
    "RST7": b"\xff\xd7",
    # Start of Frame Markers
    "SOF0": b"\xff\xc0",  # (Start of Frame | Baseline DCT)
    "SOF1": b"\xff\xc1",  # (Start of Frame | Extended Sequential DCT)
    "SOF2": b"\xff\xc2",  # (Start of Frame | Progressive DCT)
    "SOF3": b"\xff\xc3",  # (Start of Frame | Lossless JPEG)
    # Scan Headwer
    "SOS": b"\xff\xda",  # (Scan Header)
}

MARKER_SEGMENTS_JPEG_ADDRESS = {
    # Start/End of Image
    b"\xff\xd8": "SOI",  # (Start of Image)
    b"\xff\xd9": "EOI",  # (End of Image)
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
    b"\xff\xfe": "COM",  # (Comment)
    # Define Markers
    b"\xff\xdb": "DQT",  # (Define Quantization Table)
    b"\xff\xc4": "DHT",  # (Define Huffman Table)
    b"\xff\xdd": "DRI",  # (Restart Interval)
    # Restart Markers
    b"\xff\xd0": "RST0",
    b"\xff\xd1": "RST1",
    b"\xff\xd2": "RST2",
    b"\xff\xd3": "RST3",
    b"\xff\xd4": "RST4",
    b"\xff\xd5": "RST5",
    b"\xff\xd6": "RST6",
    b"\xff\xd7": "RST7",
    # Start of Frame Markers
    b"\xff\xc0": "SOF0",  # (Start of Frame | Baseline DCT)
    b"\xff\xc1": "SOF1",  # (Start of Frame | Extended Sequential DCT)
    b"\xff\xc2": "SOF2",  # (Start of Frame | Progressive DCT)
    b"\xff\xc3": "SOF3",  # (Start of Frame | Lossless JPEG)
    # Scan Header
    b"\xff\xda": "SOS",  # (Scan Header)
}
