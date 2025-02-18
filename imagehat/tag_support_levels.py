

# Types related to tags according to the EXIF standard
# These types are represented in bits/bytes
BYTE = 1 # An 8-bit unsigned integer.
ASCII = 2 # An 8-bit byte containing one 7-bit ASCII code. Final bute is terminated with NULL. 1 per character.
SHORT = 3 # A 16-bit unsigned integer.
LONG = 4 # A 32-but usinged intege.
RATIONAL = 5 # Two LONGs, first LONG is the numerator and the second LONG expresses the denominator.
SIGNED_BYTE = 6 # RARE IN TIFF. A 8-bit signed integer.
UNDEFINED = 7  # An 8-bit byte that may take any value depending on the field defenition. Often used for unstructured binary data. 
SINGED_SHORT = 8 # A 16-bit signed integer. 
SIGNED_LONG = 9 # A 32-bit signed integer. 
SIGNED_RATIONAL = 10 # Two SIGNED_LONGs values. 64-bits in total (32 + 32).
FLOAT = 11 # A 32-bit single-precision floating-point number. 
DOUBLE = 12 # A 64-bit double-precision floating-point number.
UTF_8 = 129 # An 8-bit integer representing a string according to UTF-8
SHORT_OR_LONG = [SHORT, LONG] 
ASCII_OR_UTF_8 = [ASCII, UTF_8]
ANY = [BYTE, ASCII, SHORT, LONG, RATIONAL, SIGNED_BYTE, UNDEFINED, SINGED_SHORT, SIGNED_LONG, SIGNED_RATIONAL, FLOAT, DOUBLE, UTF_8]


TAG_TYPE_SIZE_BYTES = {
    "BYTE":1,
    "UTF_8":1,
    "ASCII":1,
    "SHORT":2,
    "LONG":4,
    "RATIONAL":8,
    "SIGNED_BYTE":1,
    "UNDEFINED":1,
    "SINGED_SHORT":2,
    "SIGNED_LONG":4, 
    "SIGNED_RATIONAL":8,
    "FLOAT":4,
    "DOUBLE":8,
}

TAG_TYPES = {
    1:"BYTE",
    2:"ASCII",
    3:"SHORT",
    4:"LONG",
    5:"RATIONAL",
    6:"SIGNED_BYTE",
    7:"UNDEFINED", # Used for EXIF maker notes
    8:"SIGNED_SHORT",
    9:"SIGNED_LONG",
    10:"SIGNED_RATIONAL",
    11:"FLOAT",
    12:"DOUBLE",
    129:"UTF-8",
}

OVERFLOW_TYPES = ["RATIONAL", "SIGNED_RATIONAL", "DOUBLE"] 

# MORE_THAN_4B = ["RATIONAL", "SIGNED_RATIONAL", "DOUBLE"]

EXIF_TAGS = {
    # A. Tags Relating to Version
    "ExifVersion": {"tag": b"\x90\x00", "type": "UNDEFINED", "count": 4},
    "FlashpixVersion": {"tag": b"\xA0\x00", "type": "UNDEFINED", "count": 4},

    # B. Tag Relating to Image Data Characteristics
    "ColorSpace": {"tag": b"\xA0\x01", "type": "SHORT", "count": 1},
    "Gamma": {"tag": b"\xA5\x00", "type": "RATIONAL", "count": 1},

    # C. Tags Relating to Image Configuration
    "ComponentsConfiguration": {"tag": b"\x91\x01", "type": "UNDEFINED", "count": 4},
    "CompressedBitsPerPixel": {"tag": b"\x91\x02", "type": "RATIONAL", "count": 1},
    "PixelXDimension": {"tag": b"\xA0\x02", "type": "SHORT or LONG", "count": 1},
    "PixelYDimension": {"tag": b"\xA0\x03", "type": "SHORT or LONG", "count": 1},

    # D. Tags Relating to User Information
    "MakerNote": {"tag": b"\x92\x7C", "type": "UNDEFINED", "count": "Any"},
    "UserComment": {"tag": b"\x92\x86", "type": "UNDEFINED", "count": "Any"},

    # E. Tag Relating to Related File Information
    "RelatedSoundFile": {"tag": b"\xA0\x04", "type": "ASCII", "count": 13},

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
    "ExposureTime": {"tag": b"\x82\x9A", "type": "RATIONAL", "count": 1},
    "FNumber": {"tag": b"\x82\x9D", "type": "RATIONAL", "count": 1},
    "ExposureProgram": {"tag": b"\x88\x22", "type": "SHORT", "count": 1},
    "PhotographicSensitivity": {"tag": b"\x88\x27", "type": "SHORT", "count": "Any"},
    "ShutterSpeedValue": {"tag": b"\x92\x01", "type": "SRATIONAL", "count": 1},
    "ApertureValue": {"tag": b"\x92\x02", "type": "RATIONAL", "count": 1},
    "BrightnessValue": {"tag": b"\x92\x03", "type": "SRATIONAL", "count": 1},
    "ExposureBiasValue": {"tag": b"\x92\x04", "type": "SRATIONAL", "count": 1},
    "MeteringMode": {"tag": b"\x92\x07", "type": "SHORT", "count": 1},
    "LightSource": {"tag": b"\x92\x08", "type": "SHORT", "count": 1},
    "Flash": {"tag": b"\x92\x09", "type": "SHORT", "count": 1},
    "FocalLength": {"tag": b"\x92\x0A", "type": "RATIONAL", "count": 1},

    # H. Tags Relating to Shooting Situation
    "Temperature": {"tag": b"\x94\x00", "type": "SRATIONAL", "count": 1},
    "Humidity": {"tag": b"\x94\x01", "type": "RATIONAL", "count": 1},
    "Pressure": {"tag": b"\x94\x02", "type": "RATIONAL", "count": 1},
    "WaterDepth": {"tag": b"\x94\x03", "type": "SRATIONAL", "count": 1},
    "Acceleration": {"tag": b"\x94\x04", "type": "RATIONAL", "count": 1},
    "CameraElevationAngle": {"tag": b"\x94\x05", "type": "SRATIONAL", "count": 1},

    # I. Other Tags
    "ImageUniqueID": {"tag": b"\xA4\x20", "type": "ASCII", "count": 33},
    "CameraOwnerName": {"tag": b"\xA4\x30", "type": "ASCII or UTF-8", "count": "Any"},
    "BodySerialNumber": {"tag": b"\xA4\x31", "type": "ASCII", "count": "Any"},
    "LensSpecification": {"tag": b"\xA4\x32", "type": "RATIONAL", "count": 4},
    "LensMake": {"tag": b"\xA4\x33", "type": "ASCII or UTF-8", "count": "Any"},
    "LensModel": {"tag": b"\xA4\x34", "type": "ASCII or UTF-8", "count": "Any"},
    "LensSerialNumber": {"tag": b"\xA4\x35", "type": "ASCII", "count": "Any"},
    "ImageTitle": {"tag": b"\xA4\x36", "type": "ASCII or UTF-8", "count": "Any"},
    "Photographer": {"tag": b"\xA4\x37", "type": "ASCII or UTF-8", "count": "Any"},
    "ImageEditor": {"tag": b"\xA4\x38", "type": "ASCII or UTF-8", "count": "Any"},
    "CameraFirmware": {"tag": b"\xA4\x39", "type": "ASCII or UTF-8", "count": "Any"},
    "RAWDevelopingSoftware": {"tag": b"\xA4\x3A", "type": "ASCII or UTF-8", "count": "Any"},
    "ImageEditingSoftware": {"tag": b"\xA4\x3B", "type": "ASCII or UTF-8", "count": "Any"},
    "MetadataEditingSoftware": {"tag": b"\xA4\x3C", "type": "ASCII or UTF-8", "count": "Any"},

    # J. Tags Relating to Picture-Taking Conditions
    "ExposureTime": {"tag": b"\x82\x9A", "type": "RATIONAL", "count": 1},
    "FNumber": {"tag": b"\x82\x9D", "type": "RATIONAL", "count": 1},
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
    "ShutterSpeedValue": {"tag": b"\x92\x01", "type": "SRATIONAL", "count": 1},
    "ApertureValue": {"tag": b"\x92\x02", "type": "RATIONAL", "count": 1},
    "BrightnessValue": {"tag": b"\x92\x03", "type": "SRATIONAL", "count": 1},
    "ExposureBiasValue": {"tag": b"\x92\x04", "type": "SRATIONAL", "count": 1},
    "MaxApertureValue": {"tag": b"\x92\x05", "type": "RATIONAL", "count": 1},
    "SubjectDistance": {"tag": b"\x92\x06", "type": "RATIONAL", "count": 1},
    "MeteringMode": {"tag": b"\x92\x07", "type": "SHORT", "count": 1},
    "LightSource": {"tag": b"\x92\x08", "type": "SHORT", "count": 1},
    "Flash": {"tag": b"\x92\x09", "type": "SHORT", "count": 1},
    "FocalLength": {"tag": b"\x92\x0A", "type": "RATIONAL", "count": 1},
    "SubjectArea": {"tag": b"\x92\x14", "type": "SHORT", "count": [2, 3, 4]},
    "FlashEnergy": {"tag": b"\xA2\x0B", "type": "RATIONAL", "count": 1},
    "SpatialFrequencyResponse": {"tag": b"\xA2\x0C", "type": "UNDEFINED", "count": "Any"},
    "FocalPlaneXResolution": {"tag": b"\xA2\x0E", "type": "RATIONAL", "count": 1},
    "FocalPlaneYResolution": {"tag": b"\xA2\x0F", "type": "RATIONAL", "count": 1},
    "FocalPlaneResolutionUnit": {"tag": b"\xA2\x10", "type": "SHORT", "count": 1},
    "SubjectLocation": {"tag": b"\xA2\x14", "type": "SHORT", "count": 2},
    "ExposureIndex": {"tag": b"\xA2\x15", "type": "RATIONAL", "count": 1},
    "SensingMethod": {"tag": b"\xA2\x17", "type": "SHORT", "count": 1},
    "FileSource": {"tag": b"\xA3\x00", "type": "UNDEFINED", "count": 1},
    "SceneType": {"tag": b"\xA3\x01", "type": "UNDEFINED", "count": 1},
    "CFAPattern": {"tag": b"\xA3\x02", "type": "UNDEFINED", "count": "Any"},
    "CustomRendered": {"tag": b"\xA4\x01", "type": "SHORT", "count": 1},
    "ExposureMode": {"tag": b"\xA4\x02", "type": "SHORT", "count": 1},
    "WhiteBalance": {"tag": b"\xA4\x03", "type": "SHORT", "count": 1},
    "DigitalZoomRatio": {"tag": b"\xA4\x04", "type": "RATIONAL", "count": 1},
    "FocalLengthIn35mmFilm": {"tag": b"\xA4\x05", "type": "SHORT", "count": 1},
    "SceneCaptureType": {"tag": b"\xA4\x06", "type": "SHORT", "count": 1},
    "GainControl": {"tag": b"\xA4\x07", "type": "RATIONAL", "count": 1},
    "Contrast": {"tag": b"\xA4\x08", "type": "SHORT", "count": 1},
    "Saturation": {"tag": b"\xA4\x09", "type": "SHORT", "count": 1},
    "Sharpness": {"tag": b"\xA4\x0A", "type": "SHORT", "count": 1},
    "DeviceSettingDescription": {"tag": b"\xA4\x0B", "type": "UNDEFINED", "count": "Any"},
    "SubjectDistanceRange": {"tag": b"\xA4\x0C", "type": "SHORT", "count": 1},
    "CompositeImage": {"tag": b"\xA4\x60", "type": "SHORT", "count": 1},
    "SourceImageNumberOfCompositeImage": {"tag": b"\xA4\x61", "type": "SHORT", "count": 2},
    "SourceExposureTimesOfCompositeImage": {"tag": b"\xA4\x62", "type": "UNDEFINED", "count": "Any"},
}

EXIF_GPS_TAGS = {
    "GPSVersionID": {"tag": b"\x00", "type": "BYTE", "count": 4},
    "GPSLatitudeRef": {"tag": b"\x01", "type": "ASCII", "count": 2},
    "GPSLatitude": {"tag": b"\x02", "type": "RATIONAL", "count": 3},
    "GPSLongitudeRef": {"tag": b"\x03", "type": "ASCII", "count": 2},
    "GPSLongitude": {"tag": b"\x04", "type": "RATIONAL", "count": 3},
    "GPSAltitudeRef": {"tag": b"\x05", "type": "BYTE", "count": 1},
    "GPSAltitude": {"tag": b"\x06", "type": "RATIONAL", "count": 1},
    "GPSTimeStamp": {"tag": b"\x07", "type": "RATIONAL", "count": 3},
    "GPSSatellites": {"tag": b"\x08", "type": "ASCII", "count": "Any"},
    "GPSStatus": {"tag": b"\x09", "type": "ASCII", "count": 2},
    "GPSMeasureMode": {"tag": b"\x0A", "type": "ASCII", "count": 2},
    "GPSDOP": {"tag": b"\x0B", "type": "RATIONAL", "count": 1},
    "GPSSpeedRef": {"tag": b"\x0C", "type": "ASCII", "count": 2},
    "GPSSpeed": {"tag": b"\x0D", "type": "RATIONAL", "count": 1},
    "GPSTrackRef": {"tag": b"\x0E", "type": "ASCII", "count": 2},
    "GPSTrack": {"tag": b"\x0F", "type": "RATIONAL", "count": 1},
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
    "GPSDestDistance": {"tag": b"\x1A", "type": "RATIONAL", "count": 1},
    "GPSProcessingMethod": {"tag": b"\x1B", "type": "UNDEFINED", "count": "Any"},
    "GPSAreaInformation": {"tag": b"\x1C", "type": "UNDEFINED", "count": "Any"},
    "GPSDateStamp": {"tag": b"\x1D", "type": "ASCII", "count": 11},
    "GPSDifferential": {"tag": b"\x1E", "type": "SHORT", "count": 1},
    "GPSHPositioningError": {"tag": b"\x1F", "type": "RATIONAL", "count": 1},
}

EXIF_TAGS_REVERSED = {v["tag"]: k for k, v in EXIF_TAGS.items()}
EXIF_TAG_DICT = {**EXIF_TAGS_REVERSED}

GPS_TAGS_REVERSED = {v["tag"]: k for k, v in EXIF_GPS_TAGS.items()}
EXIF_GPS_TAGS_DICT = {**GPS_TAGS_REVERSED}


# IMPORTANT NOTE: EXIF Tags build upon the TIFF structure, but EXIF is an extension of TIFF (superset). They share the same underlying data strcuture.
# NOTE TIFF: Describes image structure and storage. Focus on internal strucuture.
# NOTE EXIF: Specifically designed for photographic metadata. 
# NOTE: ALL information is directly derived from the JEITA ISO standard documentation.

"""
# NOTE: This dictionary refers to the attribute inforamtion relating to 
TIFF_SPECIFIC_ATTRIBS = {
    # A. Tags relating to image data structure
    "ImageWidth": {
        "Dec": 256, "Hex": b"\x01\x00", "Type": SHORT_OR_LONG, "Count": 1
    },
    "ImageLength": {
        "Dec": 257, "Hex": b"\x01\x01", "Type": SHORT_OR_LONG, "Count": 1
    },
    "BitsPerSample": {
        "Dec": 258, "Hex": b"\x01\x02", "Type": SHORT, "Count": 3
    },
    "Compression": {
        "Dec": 259, "Hex": b"\x01\x03", "Type": SHORT, "Count": 1
    },
    "PhotometricInterpretation": {
        "Dec": 262, "Hex": b"\x01\x06", "Type": SHORT, "Count": 1
    },
    "Orientation": {
        "Dec": 274, "Hex": b"\x01\x12", "Type": SHORT, "Count": 1
    },
    "SamplesPerPixel": {
        "Dec": 277, "Hex": b"\x01\x15", "Type": SHORT, "Count": 1
    },
    "XResolution": {
        "Dec": 282, "Hex": b"\x01\x1A", "Type": RATIONAL, "Count": 1
    },
    "YResolution": {
        "Dec": 283, "Hex": b"\x01\x1B", "Type": RATIONAL, "Count": 1
    },
    "PlanarConfiguration": {
        "Dec": 284, "Hex": b"\x01\x1C", "Type": SHORT, "Count": 1
    },
    "ResolutionUnit": {
        "Dec": 296, "Hex": b"\x01\x28", "Type": SHORT, "Count": 1
    },
    "YCbCrSubSampling": {
        "Dec": 530, "Hex": b"\x02\x12", "Type": SHORT, "Count": 2
    },
    "YCbCrPositioning": {
        "Dec": 531, "Hex": b"\x02\x13", "Type": SHORT, "Count": 1
    },

    # B. Tags relating to recording offset
    "StripOffsets": {
        "Dec": 273, "Hex": b"\x01\x11", "Type": SHORT_OR_LONG, "Count": "*S"
    },
    "RowsPerStrip": {
        "Dec": 278, "Hex": b"\x01\x16", "Type": SHORT_OR_LONG, "Count": 1
    },
    "StripByteCounts": {
        "Dec": 279, "Hex": b"\x01\x17", "Type": SHORT_OR_LONG, "Count": "*S"
    },
    "JPEGInterchangeFormat": {
        "Dec": 513, "Hex": b"\x02\x01", "Type": LONG, "Count": 1
    },
    "JPEGInterchangeFormatLength": {
        "Dec": 514, "Hex": b"\x02\x02", "Type": LONG, "Count": 1
    },

    # C. Tags relating to image data characteristics
    "TransferFunction": {
        "Dec": 301, "Hex": b"\x01\x2D", "Type": SHORT, "Count": 3*256
    },
    "WhitePoint": {
        "Dec": 318, "Hex": b"\x01\x3E", "Type": RATIONAL, "Count": 2
    },
    "PrimaryChromaticities": {
        "Dec": 319, "Hex": b"\x01\x3F", "Type": RATIONAL, "Count": 6
    },
    "YCbCrCoefficients": {
        "Dec": 529, "Hex": b"\x02\x11", "Type": RATIONAL, "Count": 3
    },
    "ReferenceBlackWhite": {
        "Dec": 532, "Hex": b"\x02\x14", "Type": RATIONAL, "Count": 6
    },

    # D. Other tags
    "ImageDescription": {
        "Dec": 270, "Hex": b"\x01\x0E", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "Make": {
        "Dec": 271, "Hex": b"\x01\x0F", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "Model": {
        "Dec": 272, "Hex": b"\x01\x10", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "Software": {
        "Dec": 305, "Hex": b"\x01\x31", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "DateTime": {
        "Dec": 306, "Hex": b"\x01\x32", "Type": ASCII, "Count": 20
    },
    "Artist": {
        "Dec": 315, "Hex": b"\x01\x3B", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "Copyright": {
        "Dec": 33432, "Hex": b"\x82\x98", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    }
}

# NOTE: This dictionary refers to the attribute information relating to camera information
EXIF_IFD_ATTRIB_INFO_1 = { 
    "ExifVersion":{
        "Dec":36864, "Hex":b"\x90\x00", "Type":UNDEFINED, "Count":4
        },
    "FlashpixVersion":{
        "Dec":40960, "Hex":b"\xA0\x00", "Type":UNDEFINED, "Count":4
        },
    "ColorSpace":{
        "Dec":40961, "Hex":b"\xA0\x01", "Type":SHORT, "Count":1
    },
    "Gamma":{
        "Dec":42240, "Hex":b"\xA5\x00", "Type":RATIONAL, "Count":1},
    "ComponentsConfiguration": {
        "Dec": 37121, "Hex": b"\x91\x01", "Type":UNDEFINED, "Count": 4
    },
    "CompressedBitsPerPixel": {
        "Dec": 37122, "Hex": b"\x91\x02", "Type":RATIONAL, "Count": 1
    },
    "PixelXDimension": {
        "Dec": 40962, "Hex": b"\xA0\x02", "Type": SHORT_OR_LONG, "Count": 1
    },
    "PixelYDimension": {
        "Dec": 40963, "Hex": b"\xA0\x03", "Type": SHORT_OR_LONG, "Count": 1
    },
    "MakerNote": {
        "Dec": 37500, "Hex": b"\x92\x7C", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "UserComment": {
        "Dec": 37510, "Hex": b"\x92\x86", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "RelatedSoundFile": {
        "Dec": 40964, "Hex": b"\xA0\x04", "Type": ASCII, "Count": 13
    },
    "DateTimeOriginal": {
        "Dec": 36867, "Hex": b"\x90\x03", "Type": ASCII, "Count": 20
    },
    "DateTimeDigitized": {
        "Dec": 36868, "Hex": b"\x90\x04", "Type": ASCII, "Count": 20
    },
    "OffsetTime": {
        "Dec": 36880, "Hex": b"\x90\x10", "Type": ASCII, "Count": 7
    },
    "OffsetTimeOriginal": {
        "Dec": 36881, "Hex": b"\x90\x11", "Type": ASCII, "Count": 7
    },
    "OffsetTimeDigitized": {
        "Dec": 36882, "Hex": b"\x90\x12", "Type": ASCII, "Count": 7
    },
    "SubSecTime": {
        "Dec": 37520, "Hex": b"\x92\x90", "Type": ASCII, "Count": [0, 1000]
    },
    "SubSecTimeOriginal": {
        "Dec": 37521, "Hex": b"\x92\x91", "Type": ASCII, "Count": [0, 1000]
    },
    "SubSecTimeDigitized": {
        "Dec": 37522, "Hex": b"\x92\x92", "Type": ASCII, "Count": [0, 1000]
    },
    "Temperature": {
        "Dec": 37888, "Hex": b"\x94\x00", "Type": SIGNED_RATIONAL, "Count": 1
    },
    "Humidity": {
        "Dec": 37889, "Hex": b"\x94\x01", "Type": RATIONAL, "Count": 1
    },
    "Pressure": {
        "Dec": 37890, "Hex": b"\x94\x02", "Type": RATIONAL, "Count": 1
    },
    "WaterDepth": {
        "Dec": 37891, "Hex": b"\x94\x03", "Type": SIGNED_RATIONAL, "Count": 1
    },
    "Acceleration": {
        "Dec": 37892, "Hex": b"\x94\x04", "Type": RATIONAL, "Count": 1
    },
    "CameraElevationAngle": {
        "Dec": 37893, "Hex": b"\x94\x05", "Type": SIGNED_RATIONAL, "Count": 1
    },
    
    "ImageUniqueID": {
        "Dec": 42016, "Hex": b"\xA4\x20", "Type": ASCII, "Count": 33
    },
    "CameraOwnerName": {
        "Dec": 42032, "Hex": b"\xA4\x30", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "BodySerialNumber": {
        "Dec": 42033, "Hex": b"\xA4\x31", "Type": ASCII, "Count": [0, 1000]
    },
    "LensSpecification": {
        "Dec": 42034, "Hex": b"\xA4\x32", "Type": RATIONAL, "Count": 4
    },
    "LensMake": {
        "Dec": 42035, "Hex": b"\xA4\x33", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "LensModel": {
        "Dec": 42036, "Hex": b"\xA4\x34", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "LensSerialNumber": {
        "Dec": 42037, "Hex": b"\xA4\x35", "Type": ASCII, "Count": [0, 1000]
    },
    "ImageTitle": {
        "Dec": 42038, "Hex": b"\xA4\x36", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "Photographer": {
        "Dec": 42039, "Hex": b"\xA4\x37", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "ImageEditor": {
        "Dec": 42040, "Hex": b"\xA4\x38", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "CameraFirmware": {
        "Dec": 42041, "Hex": b"\xA4\x39", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "RAWDevelopingSoftware": {
        "Dec": 42042, "Hex": b"\xA4\x3A", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "ImageEditingSoftware": {
        "Dec": 42043, "Hex": b"\xA4\x3B", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    },
    "MetadataEditingSoftware": {
        "Dec": 42044, "Hex": b"\xA4\x3C", "Type": ASCII_OR_UTF_8, "Count": [0, 1000]
    }

}

# NOTE: This dictinary refers to the attribute information relating to camera
EXIF_IFD_ATTRIB_INFO_2 = {
    "ExposureTime": {
        "Dec": 33434, "Hex": b"\x82\x9A", "Type": RATIONAL, "Count": 1
    },
    "FNumber": {
        "Dec": 33437, "Hex": b"\x82\x9D", "Type": RATIONAL, "Count": 1
    },
    "ExposureProgram": {
        "Dec": 34850, "Hex": b"\x88\x22", "Type": SHORT, "Count": 1
    },
    "SpectralSensitivity": {
        "Dec": 34852, "Hex": b"\x88\x24", "Type": ASCII, "Count": [0, 1000]
    },
    "PhotographicSensitivity": {
        "Dec": 34855, "Hex": b"\x88\x27", "Type": SHORT, "Count": [0, 1000]
    },
    "OECF": {
        "Dec": 34856, "Hex": b"\x88\x28", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "SensitivityType": {
        "Dec": 34864, "Hex": b"\x88\x30", "Type": SHORT, "Count": 1
    },
    "StandardOutputSensitivity": {
        "Dec": 34865, "Hex": b"\x88\x31", "Type": LONG, "Count": 1
    },
    "RecommendedExposureIndex": {
        "Dec": 34866, "Hex": b"\x88\x32", "Type": LONG, "Count": 1
    },
    "ISOSpeed": {
        "Dec": 34867, "Hex": b"\x88\x33", "Type": LONG, "Count": 1
    },
    "ISOSpeedLatitudeyyy": {
        "Dec": 34868, "Hex": b"\x88\x34", "Type": LONG, "Count": 1
    },
    "ISOSpeedLatitudezzz": {
        "Dec": 34869, "Hex": b"\x88\x35", "Type": LONG, "Count": 1
    },
    "ShutterSpeedValue": {
        "Dec": 37377, "Hex": b"\x92\x01", "Type": SIGNED_RATIONAL, "Count": 1
    },
    "ApertureValue": {
        "Dec": 37378, "Hex": b"\x92\x02", "Type": RATIONAL, "Count": 1
    },
    "BrightnessValue": {
        "Dec": 37379, "Hex": b"\x92\x03", "Type": SIGNED_RATIONAL, "Count": 1
    },
    "ExposureBiasValue": {
        "Dec": 37380, "Hex": b"\x92\x04", "Type": SIGNED_RATIONAL, "Count": 1
    },
    "MaxApertureValue": {
        "Dec": 37381, "Hex": b"\x92\x05", "Type": RATIONAL, "Count": 1
    },
    "SubjectDistance": {
        "Dec": 37382, "Hex": b"\x92\x06", "Type": RATIONAL, "Count": 1
    },
    "MeteringMode": {
        "Dec": 37383, "Hex": b"\x92\x07", "Type": SHORT, "Count": 1
    },
    "LightSource": {
        "Dec": 37384, "Hex": b"\x92\x08", "Type": SHORT, "Count": 1
    },
    "Flash": {
        "Dec": 37385, "Hex": b"\x92\x09", "Type": SHORT, "Count": 1
    },
    "FocalLength": {
        "Dec": 37386, "Hex": b"\x92\x0A", "Type": RATIONAL, "Count": 1
    },
    "SubjectArea": {
        "Dec": 37396, "Hex": b"\x92\x14", "Type": SHORT, "Count": [2, 4]
    },
    "FlashEnergy": {
        "Dec": 41483, "Hex": b"\xA2\x0B", "Type": RATIONAL, "Count": 1
    },
    "SpatialFrequencyResponse": {
        "Dec": 41484, "Hex": b"\xA2\x0C", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "FocalPlaneXResolution": {
        "Dec": 41486, "Hex": b"\xA2\x0E", "Type": RATIONAL, "Count": 1
    },
    "FocalPlaneYResolution": {
        "Dec": 41487, "Hex": b"\xA2\x0F", "Type": RATIONAL, "Count": 1
    },
    "FocalPlaneResolutionUnit": {
        "Dec": 41488, "Hex": b"\xA2\x10", "Type": SHORT, "Count": 1
    },
    "SubjectLocation": {
        "Dec": 41492, "Hex": b"\xA2\x14", "Type": SHORT, "Count": 2
    },
    "ExposureIndex": {
        "Dec": 41493, "Hex": b"\xA2\x15", "Type": RATIONAL, "Count": 1
    },
    "SensingMethod": {
        "Dec": 41495, "Hex": b"\xA2\x17", "Type": SHORT, "Count": 1
    },
    "FileSource": {
        "Dec": 41728, "Hex": b"\xA3\x00", "Type": UNDEFINED, "Count": 1
    },
    "SceneType": {
        "Dec": 41729, "Hex": b"\xA3\x01", "Type": UNDEFINED, "Count": 1
    },
    "CFAPattern": {
        "Dec": 41730, "Hex": b"\xA3\x02", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "CustomRendered": {
        "Dec": 41985, "Hex": b"\xA4\x01", "Type": SHORT, "Count": 1
    },
    "ExposureMode": {
        "Dec": 41986, "Hex": b"\xA4\x02", "Type": SHORT, "Count": 1
    },
    "WhiteBalance": {
        "Dec": 41987, "Hex": b"\xA4\x03", "Type": SHORT, "Count": 1
    },
    "DigitalZoomRatio": {
        "Dec": 41988, "Hex": b"\xA4\x04", "Type": RATIONAL, "Count": 1
    },
    "FocalLengthIn35mmFilm": {
        "Dec": 41989, "Hex": b"\xA4\x05", "Type": SHORT, "Count": 1
    },
    "SceneCaptureType": {
        "Dec": 41990, "Hex": b"\xA4\x06", "Type": SHORT, "Count": 1
    },
    "GainControl": {
        "Dec": 41991, "Hex": b"\xA4\x07", "Type": RATIONAL, "Count": 1
    },
    "Contrast": {
        "Dec": 41992, "Hex": b"\xA4\x08", "Type": SHORT, "Count": 1
    },
    "Saturation": {
        "Dec": 41993, "Hex": b"\xA4\x09", "Type": SHORT, "Count": 1
    },
    "Sharpness": {
        "Dec": 41994, "Hex": b"\xA4\x0A", "Type": SHORT, "Count": 1
    },
    "DeviceSettingDescription": {
        "Dec": 41995, "Hex": b"\xA4\x0B", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "SubjectDistanceRange": {
        "Dec": 41996, "Hex": b"\xA4\x0C", "Type": SHORT, "Count": 1
    },
    "CompositeImage": {
        "Dec": 42080, "Hex": b"\xA4\x60", "Type": SHORT, "Count": 1
    },
    "SourceImageNumberOfCompositeImage": {
        "Dec": 42081, "Hex": b"\xA4\x61", "Type": SHORT, "Count": 2
    },
    "SourceExposureTimesOfCompositeImage": {
        "Dec": 42082, "Hex": b"\xA4\x62", "Type": UNDEFINED, "Count": [0, 1000]
    }
}

# NOTE: This dictionary refers to the attribute information relating to GPS tags
EXIF_IFD_GPS_ATTRIB_INFO = {
    "GPSVersionID": {
        "Dec": 0, "Hex": b"\x00\x00", "Type": BYTE, "Count": 4
    },
    "GPSLatitudeRef": {
        "Dec": 1, "Hex": b"\x00\x01", "Type": ASCII, "Count": 2
    },
    "GPSLatitude": {
        "Dec": 2, "Hex": b"\x00\x02", "Type": RATIONAL, "Count": 3
    },
    "GPSLongitudeRef": {
        "Dec": 3, "Hex": b"\x00\x03", "Type": ASCII, "Count": 2
    },
    "GPSLongitude": {
        "Dec": 4, "Hex": b"\x00\x04", "Type": RATIONAL, "Count": 3
    },
    "GPSAltitudeRef": {
        "Dec": 5, "Hex": b"\x00\x05", "Type": BYTE, "Count": 1
    },
    "GPSAltitude": {
        "Dec": 6, "Hex": b"\x00\x06", "Type": RATIONAL, "Count": 1
    },
    "GPSTimeStamp": {
        "Dec": 7, "Hex": b"\x00\x07", "Type": RATIONAL, "Count": 3
    },
    "GPSSatellites": {
        "Dec": 8, "Hex": b"\x00\x08", "Type": ASCII, "Count": [0, 1000]
    },
    "GPSStatus": {
        "Dec": 9, "Hex": b"\x00\x09", "Type": ASCII, "Count": 2
    },
    "GPSMeasureMode": {
        "Dec": 10, "Hex": b"\x00\x0A", "Type": ASCII, "Count": 2
    },
    "GPSDOP": {
        "Dec": 11, "Hex": b"\x00\x0B", "Type": RATIONAL, "Count": 1
    },
    "GPSSpeedRef": {
        "Dec": 12, "Hex": b"\x00\x0C", "Type": ASCII, "Count": 2
    },
    "GPSSpeed": {
        "Dec": 13, "Hex": b"\x00\x0D", "Type": RATIONAL, "Count": 1
    },
    "GPSTrackRef": {
        "Dec": 14, "Hex": b"\x00\x0E", "Type": ASCII, "Count": 2
    },
    "GPSTrack": {
        "Dec": 15, "Hex": b"\x00\x0F", "Type": RATIONAL, "Count": 1
    },
    "GPSImgDirectionRef": {
        "Dec": 16, "Hex": b"\x00\x10", "Type": ASCII, "Count": 2
    },
    "GPSImgDirection": {
        "Dec": 17, "Hex": b"\x00\x11", "Type": RATIONAL, "Count": 1
    },
    "GPSMapDatum": {
        "Dec": 18, "Hex": b"\x00\x12", "Type": ASCII, "Count": [0, 1000]
    },
    "GPSDestLatitudeRef": {
        "Dec": 19, "Hex": b"\x00\x13", "Type": ASCII, "Count": 2
    },
    "GPSDestLatitude": {
        "Dec": 20, "Hex": b"\x00\x14", "Type": RATIONAL, "Count": 3
    },
    "GPSDestLongitudeRef": {
        "Dec": 21, "Hex": b"\x00\x15", "Type": ASCII, "Count": 2
    },
    "GPSDestLongitude": {
        "Dec": 22, "Hex": b"\x00\x16", "Type": RATIONAL, "Count": 3
    },
    "GPSDestBearingRef": {
        "Dec": 23, "Hex": b"\x00\x17", "Type": ASCII, "Count": 2
    },
    "GPSDestBearing": {
        "Dec": 24, "Hex": b"\x00\x18", "Type": RATIONAL, "Count": 1
    }, 
    "GPSDestDistanceRef": {
        "Dec": 25, "Hex": b"\x00\x19", "Type": ASCII, "Count": 2
    },
    "GPSDestDistance": {
        "Dec": 26, "Hex": b"\x00\x1A", "Type": RATIONAL, "Count": 1
    },
    "GPSProcessingMethod": {
        "Dec": 27, "Hex": b"\x00\x1B", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "GPSAreaInformation": {
        "Dec": 28, "Hex": b"\x00\x1C", "Type": UNDEFINED, "Count": [0, 1000]
    },
    "GPSDateStamp": {
        "Dec": 29, "Hex": b"\x00\x1D", "Type": ASCII, "Count": 11
    },
    "GPSDifferential": {
        "Dec": 30, "Hex": b"\x00\x1E", "Type": SHORT, "Count": 1
    },
    "GPSHPositioningError": {
        "Dec": 31, "Hex": b"\x00\x1F", "Type": RATIONAL, "Count": 1
    }
}
"""