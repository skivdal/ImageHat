

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

TYPE_SIZE_BYTES = {
    BYTE:1,
    ASCII:1,
    SHORT:2,
    LONG:4,
    RATIONAL:8,
    SIGNED_BYTE:1,
    UNDEFINED:1,
    SINGED_SHORT:2,
    SIGNED_LONG:4, 
    SIGNED_RATIONAL:8,
    FLOAT:4,
    DOUBLE:8,
    UTF_8:1
}



# # Recording Notation Level
# ACCESABILITY_NOTATION = {
#     "M":"Mandatory",
#     "R":"Recommended",
#     "O":"Optional",
#     "N":"It is not allowed to record"     
# }




# IMPORTANT NOTE: EXIF Tags build upon the TIFF structure, but EXIF is an extension of TIFF (superset). They share the same underlying data strcuture.
# NOTE TIFF: Describes image structure and storage. Focus on internal strucuture.
# NOTE EXIF: Specifically designed for photographic metadata. 
# NOTE: ALL information is directly derived from the JEITA ISO standard documentation.

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

