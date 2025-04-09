# IMPORTANT NOTE: EXIF Tags build upon the TIFF structure, but EXIF is an extension of TIFF (superset).
# They share the same underlying data strcuture.
# NOTE TIFF: Describes image structure and storage. Focus on internal strucuture.
# NOTE EXIF: Specifically designed for photographic metadata.
# NOTE: ALL information is directly derived from the JEITA ISO standard documentation.
# NOTE: The first IFD (0th IFD) contains TIFF tags
# Note: The second IFD (1st IFD) contains thumbnail IFD tags. These are identical


# Types related to tags according to the EXIF standard
# These types are represented in bits/bytes
BYTE = 1  # An 8-bit unsigned integer.
ASCII = 2  # An 8-bit byte containing one 7-bit ASCII code. Final byte is terminated with NULL. 1 per character.
SHORT = 3  # A 16-bit unsigned integer.
LONG = 4  # A 32-but unsigned integer.
RATIONAL = 5  # Two LONGs, first LONG is the numerator and the second LONG expresses the denominator.
SIGNED_BYTE = 6  # RARE IN TIFF. A 8-bit signed integer.
UNDEFINED = 7  # An 8-bit byte that may take any value depending on the field defenition. Often used for unstructured binary data.
SIGNED_SHORT = 8  # A 16-bit signed integer.
SIGNED_LONG = 9  # A 32-bit signed integer.
SIGNED_RATIONAL = 10  # Two SIGNED_LONGs values. 64-bits in total (32 + 32).
FLOAT = 11  # A 32-bit single-precision floating-point number.
DOUBLE = 12  # A 64-bit double-precision floating-point number.
UTF_8 = 129  # An 8-bit integer representing a string according to UTF-8
SHORT_OR_LONG = [SHORT, LONG]
ASCII_OR_UTF_8 = [ASCII, UTF_8]
ANY = [
    BYTE,
    ASCII,
    SHORT,
    LONG,
    RATIONAL,
    SIGNED_BYTE,
    UNDEFINED,
    SIGNED_SHORT,
    SIGNED_LONG,
    SIGNED_RATIONAL,
    FLOAT,
    DOUBLE,
    UTF_8,
]


TAG_TYPE_SIZE_BYTES = {
    "BYTE": 1,
    "UTF_8": 1,
    "ASCII": 1,
    "SHORT": 2,
    "LONG": 4,
    "RATIONAL": 8,
    "SIGNED_BYTE": 1,
    "UNDEFINED": 1,
    "SIGNED": 2,
    "SIGNED_LONG": 4,
    "SIGNED_RATIONAL": 8,
    "FLOAT": 4,
    "DOUBLE": 8,
}

TAG_TYPES = {
    1: "BYTE",
    2: "ASCII",
    3: "SHORT",
    4: "LONG",
    5: "RATIONAL",
    6: "SIGNED_BYTE",
    7: "UNDEFINED",  # Used for EXIF maker notes
    8: "SIGNED_SHORT",
    9: "SIGNED_LONG",
    10: "SIGNED_RATIONAL",
    11: "FLOAT",
    12: "DOUBLE",
    129: "UTF-8",
}

# Tag types that usually are too big to be represented with a complete value in the
# EXIF IFD. The value of such tags are represented with an offset to another location
# in the binary image file.
OVERFLOW_TYPES = ["RATIONAL", "SIGNED_RATIONAL", "DOUBLE"]

# Tags directly related to EXIF
EXIF_TAGS = {
    # A. Tags Relating to Version
    "ExifVersion": {"tag": b"\x90\x00", "type": "UNDEFINED", "count": 4},
    "FlashpixVersion": {"tag": b"\xa0\x00", "type": "UNDEFINED", "count": 4},
    # B. Tag Relating to Image Data Characteristics
    "ColorSpace": {"tag": b"\xa0\x01", "type": "SHORT", "count": 1},
    "Gamma": {"tag": b"\xa5\x00", "type": "RATIONAL", "count": 1},
    # C. Tags Relating to Image Configuration
    "ComponentsConfiguration": {"tag": b"\x91\x01", "type": "UNDEFINED", "count": 4},
    "CompressedBitsPerPixel": {"tag": b"\x91\x02", "type": "RATIONAL", "count": 1},
    "PixelXDimension": {"tag": b"\xa0\x02", "type": "SHORT or LONG", "count": 1},
    "PixelYDimension": {"tag": b"\xa0\x03", "type": "SHORT or LONG", "count": 1},
    # D. Tags Relating to User Information
    "MakerNote": {"tag": b"\x92\x7c", "type": "UNDEFINED", "count": "Any"},
    "UserComment": {"tag": b"\x92\x86", "type": "UNDEFINED", "count": "Any"},
    # E. Tag Relating to Related File Information
    "RelatedSoundFile": {"tag": b"\xa0\x04", "type": "ASCII", "count": 13},
    # F. Tags Relating to Date and Time
    "DateTimeOriginal": {"tag": b"\x90\x03", "type": "ASCII", "count": 20},
    "DateTimeDigitized": {"tag": b"\x90\x04", "type": "ASCII", "count": 20},
    "OffsetTime": {"tag": b"\x90\x10", "type": "ASCII", "count": 7},
    "OffsetTimeOriginal": {"tag": b"\x90\x11", "type": "ASCII", "count": 7},
    "OffsetTimeDigitized": {"tag": b"\x90\x12", "type": "ASCII", "count": 7},
    "SubSecTime": {"tag": b"\x92\x90", "type": "ASCII", "count": "Any"},
    "SubSecTimeOriginal": {"tag": b"\x92\x91", "type": "ASCII", "count": "Any"},
    "SubSecTimeDigitized": {"tag": b"\x92\x92", "type": "ASCII", "count": "Any"},
    # G. Tags Relating to Picture-Taking Conditions
    "ExposureTime": {"tag": b"\x82\x9a", "type": "RATIONAL", "count": 1},
    "FNumber": {"tag": b"\x82\x9d", "type": "RATIONAL", "count": 1},
    "ExposureProgram": {"tag": b"\x88\x22", "type": "SHORT", "count": 1},
    "SpectralSensitivity": {"tag": b"\x88\x24", "type": "ASCII", "count": "Any"},
    "PhotographicSensitivity": {"tag": b"\x88\x27", "type": "SHORT", "count": "Any"},
    "OECF": {"tag": b"\x88\x28", "type": "UNDEFINED", "count": "Any"},
    "SensitivityType": {"tag": b"\x88\x30", "type": "SHORT", "count": 1},
    "StandardOutputSensitivity": {"tag": b"\x88\x31", "type": "LONG", "count": 1},
    "RecommendedExposureIndex": {"tag": b"\x88\x32", "type": "LONG", "count": 1},
    "ISOSpeed": {"tag": b"\x88\x33", "type": "LONG", "count": 1},
    "ISOSpeedLatitudeyyy": {"tag": b"\x88\x34", "type": "LONG", "count": 1},
    "ISOSpeedLatitudezzz": {"tag": b"\x88\x35", "type": "LONG", "count": 1},
    "ShutterSpeedValue": {"tag": b"\x92\x01", "type": "SIGNED_RATIONAL", "count": 1},
    "ApertureValue": {"tag": b"\x92\x02", "type": "RATIONAL", "count": 1},
    "BrightnessValue": {"tag": b"\x92\x03", "type": "SIGNED_RATIONAL", "count": 1},
    "ExposureBiasValue": {"tag": b"\x92\x04", "type": "SIGNED_RATIONAL", "count": 1},
    "MaxApertureValue": {"tag": b"\x92\x05", "type": "RATIONAL", "count": 1},
    "SubjectDistance": {"tag": b"\x92\x06", "type": "RATIONAL", "count": 1},
    "MeteringMode": {"tag": b"\x92\x07", "type": "SHORT", "count": 1},
    "LightSource": {"tag": b"\x92\x08", "type": "SHORT", "count": 1},
    "Flash": {"tag": b"\x92\x09", "type": "SHORT", "count": 1},
    "FocalLength": {"tag": b"\x92\x0a", "type": "RATIONAL", "count": 1},
    "SubjectArea": {"tag": b"\x92\x14", "type": "SHORT", "count": [2, 3, 4]},
    "FlashEnergy": {"tag": b"\xa2\x0b", "type": "RATIONAL", "count": 1},
    "SpatialFrequencyResponse": {
        "tag": b"\xa2\x0c",
        "type": "UNDEFINED",
        "count": "Any",
    },
    "FocalPlaneXResolution": {"tag": b"\xa2\x0e", "type": "RATIONAL", "count": 1},
    "FocalPlaneYResolution": {"tag": b"\xa2\x0f", "type": "RATIONAL", "count": 1},
    "FocalPlaneResolutionUnit": {"tag": b"\xa2\x10", "type": "SHORT", "count": 1},
    "SubjectLocation": {"tag": b"\xa2\x14", "type": "SHORT", "count": 2},
    "ExposureIndex": {"tag": b"\xa2\x15", "type": "RATIONAL", "count": 1},
    "SensingMethod": {"tag": b"\xa2\x17", "type": "SHORT", "count": 1},
    "FileSource": {"tag": b"\xa3\x00", "type": "UNDEFINED", "count": 1},
    "SceneType": {"tag": b"\xa3\x01", "type": "UNDEFINED", "count": 1},
    "CFAPattern": {"tag": b"\xa3\x02", "type": "UNDEFINED", "count": "Any"},
    "CustomRendered": {"tag": b"\xa4\x01", "type": "SHORT", "count": 1},
    "ExposureMode": {"tag": b"\xa4\x02", "type": "SHORT", "count": 1},
    "WhiteBalance": {"tag": b"\xa4\x03", "type": "SHORT", "count": 1},
    "DigitalZoomRatio": {"tag": b"\xa4\x04", "type": "RATIONAL", "count": 1},
    "FocalLengthIn35mmFilm": {"tag": b"\xa4\x05", "type": "SHORT", "count": 1},
    "SceneCaptureType": {"tag": b"\xa4\x06", "type": "SHORT", "count": 1},
    "GainControl": {"tag": b"\xa4\x07", "type": "RATIONAL", "count": 1},
    "Contrast": {"tag": b"\xa4\x08", "type": "SHORT", "count": 1},
    "Saturation": {"tag": b"\xa4\x09", "type": "SHORT", "count": 1},
    "Sharpness": {"tag": b"\xa4\x0a", "type": "SHORT", "count": 1},
    "DeviceSettingDescription": {
        "tag": b"\xa4\x0b",
        "type": "UNDEFINED",
        "count": "Any",
    },
    "SubjectDistanceRange": {"tag": b"\xa4\x0c", "type": "SHORT", "count": 1},
    "CompositeImage": {"tag": b"\xa4\x60", "type": "SHORT", "count": 1},
    "SourceImageNumberOfCompositeImage": {
        "tag": b"\xa4\x61",
        "type": "SHORT",
        "count": 2,
    },
    "SourceExposureTimesOfCompositeImage": {
        "tag": b"\xa4\x62",
        "type": "UNDEFINED",
        "count": "Any",
    },
    # H. Tags Relating to Shooting Situation
    "Temperature": {"tag": b"\x94\x00", "type": "SIGNED_RATIONAL", "count": 1},
    "Humidity": {"tag": b"\x94\x01", "type": "RATIONAL", "count": 1},
    "Pressure": {"tag": b"\x94\x02", "type": "RATIONAL", "count": 1},
    "WaterDepth": {"tag": b"\x94\x03", "type": "SIGNED_RATIONAL", "count": 1},
    "Acceleration": {"tag": b"\x94\x04", "type": "RATIONAL", "count": 1},
    "CameraElevationAngle": {"tag": b"\x94\x05", "type": "SIGNED_RATIONAL", "count": 1},
    # I. Other Tags
    "ImageUniqueID": {"tag": b"\xa4\x20", "type": "ASCII", "count": 33},
    "CameraOwnerName": {"tag": b"\xa4\x30", "type": "ASCII or UTF-8", "count": "Any"},
    "BodySerialNumber": {"tag": b"\xa4\x31", "type": "ASCII", "count": "Any"},
    "LensSpecification": {"tag": b"\xa4\x32", "type": "RATIONAL", "count": 4},
    "LensMake": {"tag": b"\xa4\x33", "type": "ASCII or UTF-8", "count": "Any"},
    "LensModel": {"tag": b"\xa4\x34", "type": "ASCII or UTF-8", "count": "Any"},
    "LensSerialNumber": {"tag": b"\xa4\x35", "type": "ASCII", "count": "Any"},
    "ImageTitle": {"tag": b"\xa4\x36", "type": "ASCII or UTF-8", "count": "Any"},
    "Photographer": {"tag": b"\xa4\x37", "type": "ASCII or UTF-8", "count": "Any"},
    "ImageEditor": {"tag": b"\xa4\x38", "type": "ASCII or UTF-8", "count": "Any"},
    "CameraFirmware": {"tag": b"\xa4\x39", "type": "ASCII or UTF-8", "count": "Any"},
    "RAWDevelopingSoftware": {
        "tag": b"\xa4\x3a",
        "type": "ASCII or UTF-8",
        "count": "Any",
    },
    "ImageEditingSoftware": {
        "tag": b"\xa4\x3b",
        "type": "ASCII or UTF-8",
        "count": "Any",
    },
    "MetadataEditingSoftware": {
        "tag": b"\xa4\x3c",
        "type": "ASCII or UTF-8",
        "count": "Any",
    },
    # Interoperability Offset
    "InteroperabilityIFDPointer": {
        "tag": b"\xa0\x05",
        "type": "LONG",
        "count": 1,
    },
}

# EXIF tags related to GPS
GPS_EXIF_TAGS = {
    "GPSVersionID": {"tag": b"\x00", "type": "BYTE", "count": 4},
    "GPSLatitudeRef": {"tag": b"\x01", "type": "ASCII", "count": 2},
    "GPSLatitude": {"tag": b"\x02", "type": "RATIONAL", "count": 3},
    "GPSLongitudeRef": {"tag": b"\x03", "type": "ASCII", "count": 2},
    "GPSLongitude": {"tag": b"\x04", "type": "RATIONAL", "count": 3},
    "GPSAltitudeRef": {"tag": b"\x05", "type": "BYTE", "count": 1},
    "GPSAltitude": {"tag": b"\x06", "type": "RATIONAL", "counts": 1},
    "GPSTimeStamp": {"tag": b"\x07", "type": "RATIONAL", "count": 3},
    "GPSSatellites": {"tag": b"\x08", "type": "ASCII", "count": "Any"},
    "GPSStatus": {"tag": b"\x09", "type": "ASCII", "count": 2},
    "GPSMeasureMode": {"tag": b"\x0a", "type": "ASCII", "count": 2},
    "GPSDOP": {"tag": b"\x0b", "type": "RATIONAL", "count": 1},
    "GPSSpeedRef": {"tag": b"\x0c", "type": "ASCII", "count": 2},
    "GPSSpeed": {"tag": b"\x0d", "type": "RATIONAL", "count": 1},
    "GPSTrackRef": {"tag": b"\x0e", "type": "ASCII", "count": 2},
    "GPSTrack": {"tag": b"\x0f", "type": "RATIONAL", "count": 1},
    "GPSImgDirectionRef": {"tag": b"\x10", "type": "ASCII", "count": 2},
    "GPSImgDirection": {"tag": b"\x11", "type": "RATIONAL", "count": 1},
    "GPSMapDatum": {"tag": b"\x12", "type": "ASCII", "count": "Any"},
    "GPSDestLatitudeRef": {"tag": b"\x13", "type": "ASCII", "count": 2},
    "GPSDestLatitude": {"tag": b"\x14", "type": "RATIONAL", "count": 3},
    "GPSDestLongitudeRef": {"tag": b"\x15", "type": "ASCII", "count": 2},
    "GPSDestLongitude": {"tag": b"\x16", "type": "RATIONAL", "count": 3},
    "GPSDestBearingRef": {"tag": b"\x17", "type": "ASCII", "count": 2},
    "GPSDestBearing": {"tag": b"\x18", "type": "RATIONAL", "count": 1},
    "GPSDestDistanceRef": {"tag": b"\x19", "type": "ASCII", "count": 2},
    "GPSDestDistance": {"tag": b"\x1a", "type": "RATIONAL", "count": 1},
    "GPSProcessingMethod": {"tag": b"\x1b", "type": "UNDEFINED", "count": "Any"},
    "GPSAreaInformation": {"tag": b"\x1c", "type": "UNDEFINED", "count": "Any"},
    "GPSDateStamp": {"tag": b"\x1d", "type": "ASCII", "count": 11},
    "GPSDifferential": {"tag": b"\x1e", "type": "SHORT", "count": 1},
    "GPSHPositioningError": {"tag": b"\x1f", "type": "RATIONAL", "count": 1},
}

# Tags related to interoperability. The tag(s) of this dictionary are set to
# indicate which type of operability standard the image follows.
# The Interop tag is supposed to be recorded inside
INTEROP_EXIF_TAGS = {
    # Attached information realted to interoperability
    "InteroperabilityIndex": {"tag": b"\x00\x01", "type": "ASCII", "count": "Any"},
    "InteroperabilityVersion": {"tag": b"\x00\x02", "type": "UNDEFINED", "count": 4},
    "RelatedImageFileFormat": {"tag": b"\x10\x00", "type": "ASCII", "count": "Any"},
    "RelatedImageWidth": {"tag": b"\x10\x01", "type": "SHORT or LONG", "count": 1},
    "RelatedImageLength": {"tag": b"\x10\x02", "type": "SHORT or LONG", "count": 1},
}

# These are TIFF specific tags that are not a part of the EXIF standard, but found in the 0th IFD header
TIFF_TAGS = {
    # A. Tags relating to image data structure
    "ImageWidth": {"tag": b"\x01\x00", "type": "SHORT or LONG", "count": 1},
    "ImageLength": {"tag": b"\x01\x01", "type": "SHORT or LONG", "count": 1},
    "BitsPerSample": {"tag": b"\x01\x02", "type": "SHORT", "count": 3},
    "Compression": {"tag": b"\x01\x03", "type": "SHORT", "count": 1},
    "PhotometricInterpretation": {"tag": b"\x01\x06", "type": "SHORT", "count": 1},
    "ImageDescription": {"tag": b"\x01\x0e", "type": "ASCII or UTF-8", "count": "Any"},
    "Make": {"tag": b"\x01\x0f", "type": "ASCII or UTF-8", "count": "Any"},
    "Model": {"tag": b"\x01\x10", "type": "ASCII or UTF-8", "count": "Any"},
    # B. Tags relating to recording offset
    "StripOffsets": {"tag": b"\x01\x11", "type": "SHORT or LONG", "count": "Any"},
    "Orientation": {"tag": b"\x01\x12", "type": "SHORT", "count": 1},
    "SamplesPerPixel": {"tag": b"\x01\x15", "type": "SHORT", "count": 1},
    "RowsPerStrip": {"tag": b"\x01\x16", "type": "SHORT or LONG", "count": 1},
    "StripByteCounts": {"tag": b"\x01\x17", "type": "SHORT or LONG", "count": "Any"},
    "XResolution": {"tag": b"\x01\x1a", "type": "RATIONAL", "count": 1},
    "YResolution": {"tag": b"\x01\x1b", "type": "RATIONAL", "count": 1},
    "PlanarConfiguration": {"tag": b"\x01\x1c", "type": "SHORT", "count": 1},
    "ResolutionUnit": {"tag": b"\x01\x28", "type": "SHORT", "count": 1},
    # C. Tags relating to image data characteristics
    "TransferFunction": {"tag": b"\x01\x2d", "type": "SHORT", "count": "768 (256×3)"},
    "Software": {"tag": b"\x01\x31", "type": "ASCII or UTF-8", "count": "Any"},
    "DateTime": {"tag": b"\x01\x32", "type": "ASCII", "count": 20},
    "Artist": {"tag": b"\x01\x3b", "type": "ASCII or UTF-8", "count": "Any"},
    "WhitePoint": {"tag": b"\x01\x3e", "type": "RATIONAL", "count": 2},
    "PrimaryChromaticities": {"tag": b"\x01\x3f", "type": "RATIONAL", "count": 6},
    # JPEG thumbnail support
    "JPEGInterchangeFormat": {"tag": b"\x02\x01", "type": "LONG", "count": 1},
    "JPEGInterchangeFormatLength": {"tag": b"\x02\x02", "type": "LONG", "count": 1},
    # YCbCr-related
    "YCbCrCoefficients": {"tag": b"\x02\x11", "type": "RATIONAL", "count": 3},
    "YCbCrSubSampling": {"tag": b"\x02\x12", "type": "SHORT", "count": 2},
    "YCbCrPositioning": {"tag": b"\x02\x13", "type": "SHORT", "count": 1},
    "ReferenceBlackWhite": {"tag": b"\x02\x14", "type": "RATIONAL", "count": 6},
    # D. Other Tags
    "Copyright": {"tag": b"\x82\x98", "type": "ASCII or UTF-8", "count": "Any"},
    # Pointers
    "ExifIFDPointer": {"tag": b"\x87\x69", "type": "LONG", "count": 1},
    "GPSInfoIFDPointer": {"tag": b"\x88\x25", "type": "LONG", "count": 1},
}

TIFF_TAG_DICT_REV = {v["tag"]: k for k, v in TIFF_TAGS.items()}

EXIF_TAG_DICT_REV = {v["tag"]: k for k, v in {**EXIF_TAGS, **INTEROP_EXIF_TAGS}.items()}

INTEROP_TAG_DICT_REV = {v["tag"]: k for k, v in INTEROP_EXIF_TAGS.items()}

GPS_TAG_DICT_REV = {v["tag"]: k for k, v in GPS_EXIF_TAGS.items()}
