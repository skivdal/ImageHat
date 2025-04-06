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
