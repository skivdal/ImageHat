# This module defines strcutured metadata tag support levels used for evaluating EXIF Conformity Score.
# NOTE that the GPS IFD is purely optional and will not be utlizied in the ECS calculations.
# NOTE that the even though the Thumbnail IFD tags are equal to that of TIFF tags, they have different
# support levels that need to be split into different dictionaries.


TIFF_SUPPORT_LEVELS = {
    # A. Tags relating to image data structure
    "ImageWidth": {
        "tag": b"\x01\x00",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "ImageLength": {
        "tag": b"\x01\x01",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "BitsPerSample": {
        "tag": b"\x01\x02",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "Compression": {
        "tag": b"\x01\x03",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "PhotometricInterpretation": {
        "tag": b"\x01\x06",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "N",
        },
    },
    "ImageDescription": {
        "tag": b"\x01\x0e",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "Make": {
        "tag": b"\x01\x0f",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "Model": {
        "tag": b"\x01\x10",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    # B. Tags relating to recording offset
    "StripOffsets": {
        "tag": b"\x01\x11",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "N",
        },
    },
    "Orientation": {
        "tag": b"\x01\x12",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "SamplesPerPixel": {
        "tag": b"\x01\x15",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "RowsPerStrip": {
        "tag": b"\x01\x16",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "N",
        },
    },
    "StripByteCounts": {
        "tag": b"\x01\x17",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "N",
        },
    },
    "XResolution": {
        "tag": b"\x01\x1a",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "YResolution": {
        "tag": b"\x01\x1b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "PlanarConfiguration": {
        "tag": b"\x01\x1c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "M", "ycc": "O"},
            "compressed": "J",
        },
    },
    "ResolutionUnit": {
        "tag": b"\x01\x28",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    # C. Tags relating to image data characteristics
    "TransferFunction": {
        "tag": b"\x01\x2d",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Software": {
        "tag": b"\x01\x31",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "DateTime": {
        "tag": b"\x01\x32",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "Artist": {
        "tag": b"\x01\x3b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "WhitePoint": {
        "tag": b"\x01\x3e",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "PrimaryChromaticities": {
        "tag": b"\x01\x3f",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    # JPEG thumbnail support
    "JPEGInterchangeFormat": {
        "tag": b"\x02\x01",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "N",
        },
    },
    "JPEGInterchangeFormatLength": {
        "tag": b"\x02\x02",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "N",
        },
    },
    # YCbCr-related
    "YCbCrCoefficients": {
        "tag": b"\x02\x11",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "YCbCrSubSampling": {
        "tag": b"\x02\x12",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "J"},
            "compressed": "M",
        },
    },
    "YCbCrPositioning": {
        "tag": b"\x02\x13",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "M",
        },
    },
    "ReferenceBlackWhite": {
        "tag": b"\x02\x14",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    # D. Other Tags
    "Copyright": {
        "tag": b"\x82\x98",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    # Pointers
    "ExifIFDPointer": {
        "tag": b"\x87\x69",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "M",
        },
    },
    "GPSInfoIFDPointer": {
        "tag": b"\x88\x25",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
}


EXIF_SUPPORT_LEVELS = {
    "ExposureTime": {
        "tag": b"\x82\x9a",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "FNumber": {
        "tag": b"\x82\x9d",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ExposureProgram": {
        "tag": b"\x88\x22",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SpectralSensitivity": {
        "tag": b"\x88\x24",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "PhotographicSensitivity": {
        "tag": b"\x88\x27",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "OECF": {
        "tag": b"\x88\x28",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SensitivityType": {
        "tag": b"\x88\x30",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "StandardOutputSensitivity": {
        "tag": b"\x88\x31",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "RecommendedExposureIndex": {
        "tag": b"\x88\x32",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ISOSpeed": {
        "tag": b"\x88\x33",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ISOSpeedLatitudeyyy": {
        "tag": b"\x88\x34",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ISOSpeedLatitudezzz": {
        "tag": b"\x88\x35",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ExifVersion": {
        "tag": b"\x90\x00",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "M",
        },
    },
    "DateTimeOriginal": {
        "tag": b"\x90\x03",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "DateTimeDigitized": {
        "tag": b"\x90\x04",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "OffsetTime": {
        "tag": b"\x90\x10",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "OffsetTimeOriginal": {
        "tag": b"\x90\x11",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "OffsetTimeDigitized": {
        "tag": b"\x90\x12",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ComponentsConfiguration": {
        "tag": b"\x91\x01",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "M"},
            "compressed": "N",
        },
    },
    "CompressedBitsPerPixel": {
        "tag": b"\x91\x02",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "O"},
            "compressed": "N",
        },
    },
    "ShutterSpeedValue": {
        "tag": b"\x92\x01",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ApertureValue": {
        "tag": b"\x92\x02",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "BrightnessValue": {
        "tag": b"\x92\x03",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ExposureBiasValue": {
        "tag": b"\x92\x04",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "MaxApertureValue": {
        "tag": b"\x92\x05",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SubjectDistance": {
        "tag": b"\x92\x06",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "MeteringMode": {
        "tag": b"\x92\x07",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "LightSource": {
        "tag": b"\x92\x08",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Flash": {
        "tag": b"\x92\x09",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "FocalLength": {
        "tag": b"\x92\x0a",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SubjectArea": {
        "tag": b"\x92\x14",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "MakerNote": {
        "tag": b"\x92\x7c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "UserComment": {
        "tag": b"\x92\x86",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SubSecTime": {
        "tag": b"\x92\x90",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SubSecTimeOriginal": {
        "tag": b"\x92\x91",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SubSecTimeDigitized": {
        "tag": b"\x92\x92",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Temperature": {
        "tag": b"\x94\x00",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Humidity": {
        "tag": b"\x94\x01",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Pressure": {
        "tag": b"\x94\x02",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "WaterDepth": {
        "tag": b"\x94\x03",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Acceleration": {
        "tag": b"\x94\x04",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "CameraElevationAngle": {
        "tag": b"\x94\x05",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ImageTitle": {
        "tag": b"\xa4\x36",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Photographer": {
        "tag": b"\xa4\x37",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ImageEditor": {
        "tag": b"\xa4\x38",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "CameraFirmware": {
        "tag": b"\xa4\x39",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "RAWDevelopingSoftware": {
        "tag": b"\xa4\x3a",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ImageEditingSoftware": {
        "tag": b"\xa4\x3b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "MetadataEditingSoftware": {
        "tag": b"\xa4\x3c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "FlashpixVersion": {
        "tag": b"\xa0\x00",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ColorSpace": {
        "tag": b"\xa0\x01",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "M",
        },
    },
    "PixelXDimension": {
        "tag": b"\xa0\x02",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "M",
        },
    },
    "PixelYDimension": {
        "tag": b"\xa0\x03",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "M",
        },
    },
    "RelatedSoundFile": {
        "tag": b"\xa0\x04",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "InteroperabilityIFDPointer": {
        "tag": b"\xa0\x05",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "O",
        },
    },
    "FlashEnergy": {
        "tag": b"\xa2\x0b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SpatialFrequencyResponse": {
        "tag": b"\xa2\x0c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "FocalPlaneXResolution": {
        "tag": b"\xa2\x0e",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "FocalPlaneYResolution": {
        "tag": b"\xa2\x0f",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "FocalPlaneResolutionUnit": {
        "tag": b"\xa2\x10",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SubjectLocation": {
        "tag": b"\xa2\x14",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ExposureIndex": {
        "tag": b"\xa2\x15",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SensingMethod": {
        "tag": b"\xa2\x17",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "FileSource": {
        "tag": b"\xa3\x00",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SceneType": {
        "tag": b"\xa3\x01",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "CFAPattern": {
        "tag": b"\xa3\x02",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "CustomRendered": {
        "tag": b"\xa4\x01",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ExposureMode": {
        "tag": b"\xa4\x02",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "WhiteBalance": {
        "tag": b"\xa4\x03",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "DigitalZoomRatio": {
        "tag": b"\xa4\x04",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "FocalLengthIn35mmFilm": {
        "tag": b"\xa4\x05",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SceneCaptureType": {
        "tag": b"\xa4\x06",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "GainControl": {
        "tag": b"\xa4\x07",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Contrast": {
        "tag": b"\xa4\x08",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Saturation": {
        "tag": b"\xa4\x09",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Sharpness": {
        "tag": b"\xa4\x0a",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "DeviceSettingDescription": {
        "tag": b"\xa4\x0b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SubjectDistanceRange": {
        "tag": b"\xa4\x0c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ImageUniqueID": {
        "tag": b"\xa4\x20",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "CameraOwnerName": {
        "tag": b"\xa4\x30",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "BodySerialNumber": {
        "tag": b"\xa4\x31",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "LensSpecification": {
        "tag": b"\xa4\x32",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "LensMake": {
        "tag": b"\xa4\x33",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "LensModel": {
        "tag": b"\xa4\x34",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "LensSerialNumber": {
        "tag": b"\xa4\x35",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "CompositeImage": {
        "tag": b"\xa4\x60",
        "support": {
            "uncompressed": {"chunky": "R", "planar": "R", "ycc": "R"},
            "compressed": "R",
        },
    },
    "SourceImageNumberOfCompositeImage": {
        "tag": b"\xa4\x61",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SourceExposureTimesOfCompositeImage": {
        "tag": b"\xa4\x62",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Gamma": {
        "tag": b"\xa5\x00",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
}


GPS_SUPPORT_LEVELS = {
    "GPSVersionID": {
        "tag": b"\x00\x00",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSLatitudeRef": {
        "tag": b"\x00\x01",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSLatitude": {
        "tag": b"\x00\x02",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSLongitudeRef": {
        "tag": b"\x00\x03",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSLongitude": {
        "tag": b"\x00\x04",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSAltitudeRef": {
        "tag": b"\x00\x05",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSAltitude": {
        "tag": b"\x00\x06",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSTimeStamp": {
        "tag": b"\x00\x07",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSSatellites": {
        "tag": b"\x00\x08",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSStatus": {
        "tag": b"\x00\x09",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSMeasureMode": {
        "tag": b"\x00\x0a",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDOP": {
        "tag": b"\x00\x0b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSSpeedRef": {
        "tag": b"\x00\x0c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSSpeed": {
        "tag": b"\x00\x0d",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSTrackRef": {
        "tag": b"\x00\x0e",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSTrack": {
        "tag": b"\x00\x0f",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSImgDirectionRef": {
        "tag": b"\x00\x10",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSImgDirection": {
        "tag": b"\x00\x11",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSMapDatum": {
        "tag": b"\x00\x12",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestLatitudeRef": {
        "tag": b"\x00\x13",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestLatitude": {
        "tag": b"\x00\x14",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestLongitudeRef": {
        "tag": b"\x00\x15",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestLongitude": {
        "tag": b"\x00\x16",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestBearingRef": {
        "tag": b"\x00\x17",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestBearing": {
        "tag": b"\x00\x18",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestDistanceRef": {
        "tag": b"\x00\x19",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDestDistance": {
        "tag": b"\x00\x1a",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSProcessingMethod": {
        "tag": b"\x00\x1b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSAreaInformation": {
        "tag": b"\x00\x1c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDateStamp": {
        "tag": b"\x00\x1d",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSDifferential": {
        "tag": b"\x00\x1e",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSHPositioningError": {
        "tag": b"\x00\x1f",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
}

INTEROP_SUPPORT_LEVELS = {
    "InteroperabilityIndex": {
        "tag": b"\x00\x01",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "O",
        },
    },
    "InteroperabilityVersion": {
        "tag": b"\x00\x02",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "RelatedImageFileFormat": {
        "tag": b"\x10\x00",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "RelatedImageWidth": {
        "tag": b"\x10\x01",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "RelatedImageLength": {
        "tag": b"\x10\x02",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
}

THUMBNAIL_SUPPORT_LEVEL = {
    "ImageWidth": {
        "tag": b"\x01\x00",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "ImageLength": {
        "tag": b"\x01\x01",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "BitsPerSample": {
        "tag": b"\x01\x02",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "Compression": {
        "tag": b"\x01\x03",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "M",
        },
    },
    "PhotometricInterpretation": {
        "tag": b"\x01\x06",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "ImageDescription": {
        "tag": b"\x01\x0e",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Make": {
        "tag": b"\x01\x0f",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Model": {
        "tag": b"\x01\x10",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "StripOffsets": {
        "tag": b"\x01\x11",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "N",
        },
    },
    "Orientation": {
        "tag": b"\x01\x12",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "SamplesPerPixel": {
        "tag": b"\x01\x15",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "J",
        },
    },
    "RowsPerStrip": {
        "tag": b"\x01\x16",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "N",
        },
    },
    "StripByteCounts": {
        "tag": b"\x01\x17",
        "support": {
            "uncompressed": {"chunky": "M", "planar": "M", "ycc": "M"},
            "compressed": "N",
        },
    },
    "XResolution": {
        "tag": b"\x01\x1a",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "YResolution": {
        "tag": b"\x01\x1b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "PlanarConfiguration": {
        "tag": b"\x01\x1c",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "M", "ycc": "O"},
            "compressed": "J",
        },
    },
    "ResolutionUnit": {
        "tag": b"\x01\x28",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "TransferFunction": {
        "tag": b"\x01\x2d",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Software": {
        "tag": b"\x01\x31",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "DateTime": {
        "tag": b"\x01\x32",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Artist": {
        "tag": b"\x01\x3b",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "WhitePoint": {
        "tag": b"\x01\x3e",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "PrimaryChromaticities": {
        "tag": b"\x01\x3f",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "JPEGInterchangeFormat": {
        "tag": b"\x02\x01",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "M",
        },
    },
    "JPEGInterchangeFormatLength": {
        "tag": b"\x02\x02",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "N"},
            "compressed": "M",
        },
    },
    "YCbCrCoefficients": {
        "tag": b"\x02\x11",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "O"},
            "compressed": "O",
        },
    },
    "YCbCrSubSampling": {
        "tag": b"\x02\x12",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "M"},
            "compressed": "J",
        },
    },
    "YCbCrPositioning": {
        "tag": b"\x02\x13",
        "support": {
            "uncompressed": {"chunky": "N", "planar": "N", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ReferenceBlackWhite": {
        "tag": b"\x02\x14",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "Copyright": {
        "tag": b"\x82\x98",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "ExifIFDPointer": {
        "tag": b"\x87\x69",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
    "GPSInfoIFDPointer": {
        "tag": b"\x88\x25",
        "support": {
            "uncompressed": {"chunky": "O", "planar": "O", "ycc": "O"},
            "compressed": "O",
        },
    },
}

ALL_SUPPORT_LEVELS = {**EXIF_SUPPORT_LEVELS, **GPS_SUPPORT_LEVELS, **INTEROP_SUPPORT_LEVELS}

