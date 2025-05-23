import os
import os.path
import struct
from rich.pretty import pprint as rich_print
from imagehat.parsers.base_parser import BaseParser
from imagehat.identifiers.extensions import VALID_EXTENSIONS


from imagehat.identifiers.jpeg_specific_identifiers import (
    IDENTIFIERS,
    EXIF_IFD_POINTERS,
)
from imagehat.identifiers.jpeg_marker_segments import (
    MARKER_SEGMENTS_JPEG_ADDRESS,
)
from imagehat.identifiers.exif_attribute_information import (
    TAG_TYPES,
    OVERFLOW_TYPES,
    EXIF_TAG_DICT_REV,
    GPS_TAG_DICT_REV,
    INTEROP_TAG_DICT_REV,
    TIFF_TAG_DICT_REV,
    ALL_TAGS,
    ALL_TAGS_REV,
    ALL_EXIF_TAGS,
    TAG_TYPE_SIZE_BYTES,
    RATIONAL_TYPES,
)
from imagehat.identifiers.exif_support_levels import ALL_SUPPORT_LEVELS
from imagehat.identifiers.iptc_attribute_information import (
    IPTC_TAGS,
)

from imagehat.utils.metrics import (
    calculate_ECS,
    calculate_tag_validity_score,
    calculate_lazy_TOS,
    calculate_strict_TOS,
    calculate_header_validity,
)


class JPEGParser(BaseParser):
    """
    The JPEGParser class is a sub class of the ImageHat super class. It is designed to analyze binary image files and
    extract EXIF metadata directly from from binary image files. It supports methods for parsing JPEG, extracting EXIF
    data, and - most importantly - converting raw bytes represented as hexadecimals in order to parse structured information
    from bytes.

    Example Usage:
    --------------
    ```
    >>> image = JPEGParser("sample.jpg")
    >>> markers = image.get_image_data(verbose="exif")
    >>> print(markers)
    ```

    ```
    >>> testset_folder = os.path.join("tests", "testsets", "testset-small")
    >>> exif_dicts = JPEGParser.get_image_datas(testset_folder)
    ```
    """

    def __init__(self, img_path: str):
        # Functionality specific attributes
        self.img_path: str = img_path
        self._validate_file_path()
        self.binary_repr: bytes = self.get_binary_data()
        # Data specific attributes
        self.marker_info: dict | None = None
        self._APP1_SEGMENT: dict | None = None
        self._APP13_SEGMENT: dict | None = None
        self.file_data: dict | None = None
        self.app1_data: dict | None = None
        self.first_ifd_data: dict | None = None
        self.exif_ifd_data: dict | None = None
        self.gps_ifd_data: dict | None = None
        self.interop_ifd_data: dict | None = None
        self.thumbnail_ifd_data: dict | None = None

        # Metrics
        self.header_validity_score: float | None = None
        self.tag_validity_score: float | None = None
        self.weak_tag_order_score: float | None = None
        self.strict_tag_order_score: float | None = None
        self.ecs: float | None = None  # Final score

    def get_binary_data(self) -> bytes:
        """
        Method for fetching image data as binary array.

        :return: Image files in binary representation.
        :rtype: bytes
        """
        try:
            with open(self.img_path, "rb") as binary_repr:
                binary_content: bytes = binary_repr.read()
                if not isinstance(binary_content, bytes):
                    binary_content = binary_content.tobytes()
                return binary_content
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}") from e

    def _validate_file_path(self) -> None:
        """
        This method is used for validating the file paths, reducing the chance of error during initializing.
        Takes no parameters and is void.
        """
        if not isinstance(self.img_path, str):
            raise TypeError("Not valid type, must be string.")

        if not os.path.exists(self.img_path):
            raise FileNotFoundError(
                f"The file '{self.img_path}' does not exist or is located elsewhere."
            )

        _, ext = os.path.splitext(self.img_path)
        if ext.lower() not in ((".jpg", ".jpeg")):
            raise ValueError(
                f"Invalid file format '{ext}'. Supported formats: .jpg, .jpeg."
            )

        try:
            with open(self.img_path, "rb") as f:
                header = f.read(2)  # JPEG files start with 0xFFD8
                if header != b"\xff\xd8":
                    raise ValueError(
                        "[ERROR] Skipping file: Not a valid JPEG (invalid SOI marker)"
                    )
        except Exception as e:
            print(f"Error reading file: {e}")

    def __str__(self) -> str:
        """
        Method used to show basic information the JPEGParser object.
        """
        return f"Image: {self.img_path}, Size: {len(self.binary_repr)} bytes"

    def segment_data(self, end: int, start: int | None = None) -> None:
        """
        Metod for printing the whole byte array. Should be avoided as printed byte arrays are living nightmares.

        :return: a segment of self.binary_repr
        """
        if start is None:
            return self.binary_repr[:end]
        return self.binary_repr[start:end]

    @classmethod
    def help(cls) -> None:
        """
        Prints help for class overview and method usage.

        Example usage:
            >>> ImageHat.help()
        """
        print(help(cls))
        print(cls.__doc__.strip())
        print(cls.help.__doc__.strip())

    def _read_jpeg_markers(self) -> dict:
        """
        Identifies and extracts key JPEG markers in the binary image.

        This method scans the binary representation of the image to locate JPEG markers,
        count their occurrences, and determine their byte offsets.

        :return: A dictionary where keys represent marker names, and values contain marker-specific
                metadata, including occurrence count and byte offsets.
        :rtype: dict
        """
        try:
            pos = 0
            markers = {}

            while pos < len(self.binary_repr):
                # Ensure we are at a marker (0xFF)
                if self.binary_repr[pos] != 0xFF:
                    pos += 1
                    continue

                # Get the marker byte
                marker_byte = self.binary_repr[pos + 1]
                if marker_byte == 0x00:  # Skip padding bytes
                    pos += 2
                    continue

                marker = bytes([0xFF, marker_byte])

                # Handle restart markers (RST0-RST7)
                if 0xD0 <= marker_byte <= 0xD7:
                    marker_name = f"RST{marker_byte - 0xD0}"
                    markers[marker_name] = {
                        "offset": pos,
                        "size": None,  # RST markers are standalone and have no segment size
                    }
                    pos += 2
                    continue

                # Get marker name
                marker_name = MARKER_SEGMENTS_JPEG_ADDRESS.get(
                    marker, f"Unknown_{marker.hex().upper()}"
                )

                # Avoid duplicate markers
                if marker_name in markers:
                    marker_name = f"{marker_name}_{len(markers)}"

                # SOI and EOI markers have no size
                if marker in [b"\xff\xd8", b"\xff\xd9"]:
                    markers[marker_name] = {
                        "offset": pos,
                        "size": None,
                    }
                    pos += 2
                    continue

                # Ensure we have enough bytes to read the segment size
                if pos + 4 > len(self.binary_repr):
                    # print(f"[WARN] Incomplete marker at position {pos}. Skipping.")
                    break

                # Read segment size (2 bytes after the marker)
                segment_size = int.from_bytes(
                    self.binary_repr[pos + 2 : pos + 4], "big"
                )
                segment_end = pos + 2 + segment_size

                # Ensure the segment does not exceed the file length
                if segment_end > len(self.binary_repr):
                    # print(f"[WARN] Segment at position {pos} exceeds file length. Skipping.")
                    break

                # Record marker information
                markers[marker_name] = {
                    "offset": pos,
                    "size": segment_size,
                }

                # Move to the next marker
                pos = segment_end
            return markers

        except Exception as e:
            return {"[ERROR]": f"Failed to parse JPEG marker segments: {e}"}

    def _read_app1_segment(self, app1_offset: int) -> dict:
        """
        Locates the APP1 segment and the records its metadata content.
        The APP1 segment is commonly used for **EXIF metadata storage**.

        :param app1_offset: The bute offset where the APP1 segment starts in the image binary.
        :type app1_offset: int

        :return: A dictionary containing details about the APP1 segment, such as its
                 size, position, structural integrity, but also .
        :rtype: dict
        """
        # try:
        report = {}

        # Recording APP1 segment size (s.b. 2 bytes)
        app1_size = int.from_bytes(
            self.binary_repr[app1_offset + 2 : app1_offset + 4], byteorder="big"
        )
        if app1_offset + app1_size > len(self.binary_repr):
            raise ValueError("APP1 segment size exceeds image binary length.")

        report["APP1 Size"] = app1_size  # For latter, add failsafe if segment > 64 kb

        # Recording start of APP1 segment
        app1_location_start = app1_offset
        report["Start of APP1"] = app1_location_start

        # Recording end of APP1 segment
        app1_location_end = app1_offset + app1_size
        report["End of APP1"] = app1_location_end
        self._APP1_SEGMENT = self.binary_repr[
            app1_location_start : app1_location_start + app1_size
        ]

        if IDENTIFIERS["xmp_header"] in self._APP1_SEGMENT[:200]:
            return {"error": "Includes XMP data."}

        # Recording EXIF identifier (s.b. 4 bytes, 6 bytes including padding)
        exif_identifier = self._APP1_SEGMENT.find(IDENTIFIERS["exif_identifier"])
        report["EXIF Identifier Offset"] = (
            exif_identifier if exif_identifier != -1 else None
        )

        # Recording byte order (should be 2 bytes)
        # Recodring endianness starts here. EXIF is big-endian until byte-order is discovered.
        byte_order_offset, detected_byte_order = self._find_target_byte(
            self._APP1_SEGMENT[:25], targets=[IDENTIFIERS["II"], IDENTIFIERS["MM"]]
        )

        # if missing, assume 'MM'
        if detected_byte_order is None:
            byte_order_bytes = b"MM"  # Default assumption
            byte_order_offset = -1  # Optional: indicate it was assumed
            endianness = ">"
            report["Byte Order"] = byte_order_bytes
            report["Byte Order Offset"] = byte_order_offset
            # print("[WARN]: Byte Order not detected in this media file.")
        elif detected_byte_order:
            byte_order_bytes = self._APP1_SEGMENT[
                byte_order_offset : byte_order_offset + 2
            ]
            # Setting endianness for the rest of runtime
            endianness = "<" if byte_order_bytes == IDENTIFIERS["II"] else ">"
            report["Byte Order"] = repr(detected_byte_order)
            report["Byte Order Offset"] = byte_order_offset

        # Recording magic number (should be 2 bytes)
        magic_number = self._convert_internal_identifier(
            endianness, "H", "tiff_magic_number"
        )
        magic_number_offset = self._APP1_SEGMENT.find(magic_number)
        magic_number_bytes = self._APP1_SEGMENT[
            magic_number_offset : magic_number_offset + 2
        ]
        magic_number = struct.unpack(f"{endianness}H", magic_number_bytes)[0]
        report["TIFF Magic Number Offset"] = (
            magic_number_offset if magic_number_offset != -1 else None
        )

        ### Extremely important NOTE. All markers and tags in the JEITA documentations are displayed in MSB.
        ### Always unpack constants in big endian from project files.

        # Recording offset to first IDF (should be 4 bytes)
        ifd_temp = self._convert_internal_identifier(
            endianness=endianness, datatype="I", id="offset_first_ifd"
        )
        ifd_offset = self._APP1_SEGMENT.find(ifd_temp)
        ifd_offset_bytes = self._APP1_SEGMENT[ifd_offset : ifd_offset + 4]
        ifd_start = (
            byte_order_offset + struct.unpack(f"{endianness}I", ifd_offset_bytes)[0]
        )

        # Entries recorded within the 0th IFD
        ifd_entries = struct.unpack(
            f"{endianness}H", self._APP1_SEGMENT[ifd_start : ifd_start + 2]
        )[0]
        report["0th IFD Offset"] = ifd_offset
        report["Entries in 0th IFD"] = ifd_entries

        # Recording the 0th tags. NOTE: Most important, do not touch.
        # The 0th IFD includes Image Related tags, pointer to the GPS IFD and the EXIF IFD.
        if report["0th IFD Offset"]:
            first_ifd_info, tiff_data = self._read_first_ifd(
                ifd_start=ifd_start,
                num_entries=ifd_entries,
                tiff_header_offset=byte_order_offset,
                endianness=endianness,
            )
            report["0th IFD Information"] = first_ifd_info
            report["0th IFD Data"] = tiff_data
            self.first_ifd_data = tiff_data

        # Recoring the EXIF IFD.
        # The EXIF IFD includes Camera Device Realted tags, pointer to the Interoperability IFD.
        exif_ifd_info = None
        if first_ifd_info is not None and first_ifd_info["Offset to EXIF IFD"]:
            exif_ifd_info, exif_data = self._read_exif_ifd(
                ifd_start=first_ifd_info["Offset to EXIF IFD"],
                num_entries=first_ifd_info["Number of EXIF Entries"],
                tiff_header_offset=byte_order_offset,
                endianness=endianness,
            )
            report["EXIF IFD Info"] = exif_ifd_info
            report["EXIF IFD Data"] = exif_data
            self.exif_ifd_data = exif_data

        # Recoring the GPS EXIF tags.
        if first_ifd_info is not None and first_ifd_info["Offset to GPS IFD"]:
            gps_data = self._read_gps_ifd(
                ifd_start=first_ifd_info["Offset to GPS IFD"],
                num_entries=first_ifd_info["Number of GPS Entries"],
                tiff_header_offset=byte_order_offset,
                endianness=endianness,
            )
            report["GPS IFD Data"] = gps_data

            self.gps_ifd_data = gps_data

        # Recoring the GPS EXIF tags.
        if exif_ifd_info is not None and exif_ifd_info.get("Offset to Interop IFD"):
            interop_data = self._read_interop_ifd(
                ifd_start=exif_ifd_info["Offset to Interop IFD"],
                num_entries=exif_ifd_info["Number of Interop Entries"],
                tiff_header_offset=byte_order_offset,
                endianness=endianness,
            )
            report["Interop IFD Data"] = interop_data
            self.interop_ifd_data = interop_data

        # Recording the Thumbnail TIFF Tags.
        if first_ifd_info is not None and first_ifd_info["Offset to 1st IFD"]:
            thumbnail_data = self._read_thumbnail_ifd(
                ifd_start=first_ifd_info["Offset to 1st IFD"],
                num_entries=first_ifd_info["Number of 1st IFD Entries"],
                tiff_header_offset=byte_order_offset,
                endianness=endianness,
            )
            report["1st IFD Data"] = thumbnail_data
            self.thumbnail_ifd_data = thumbnail_data

        return report
        # except Exception as e:
        #     return {"[ERROR]": f"Failed to parse APP1 segment: {e}"}

    def _find_target_byte(self, data: bytes, targets: list[bytes]) -> None | int | str:
        """
        Helper method primarily used to find the byte order and its current location in the binary data.

        :param data: Data segment of self.binary_repr. Set to next 25 bytes as a random, large enough int.
        :type data: bytes
        :param targets: List of bytes. Should recieve byte representation of MM or II.
        :type: tagrets: List[bytes]

        :return: Returns a index of the byte that was located, along with the byte itself.
                 Return None if not found.
        :rtype: int, byte, None
        """
        for target in targets:
            index = data.find(target)
            if index != -1:
                return index, target
        return None, None

    def _convert_internal_identifier(
        self, endianness: str, datatype: str, id: str
    ) -> bytes:
        """
        Helper method that mitigates errors caused by incosistent representation of byte sequences.
        As of standard, the JEITA documentation states that all tags should be represented as big endian [MM]
        until other is stated. The tags in identifiers are also stored in big endian format, thus raises the
        need for a helper methods that converts bytes if there are mitmatches in endianness.

        :param endianness: The byte order detected (">" for big-endian, "<" for little-endian).
        :type endianness: str
        :param datatype: Byte size expected based on the format characters of the struct library.
        :type datatype: str
        :param id: Identifier based on the naming in the identifiers module.
        :type id: str

        :return: bytes packed from int based on the detected endianness.
        :rtype: bytes
        """
        if id not in IDENTIFIERS:
            raise KeyError(
                f"Identifier '{id}' not found in IDENTIFIERS."
            )  # Raises key error if identifier not found

        if endianness == ">":
            return IDENTIFIERS[id]  # Big-endian

        unpacked_value = struct.unpack(f">{datatype}", IDENTIFIERS[id])[
            0
        ]  # Unpack in big-endian
        return struct.pack(
            f"{endianness}{datatype}", unpacked_value
        )  # Repack value according to correct endianness

    def _read_first_ifd(
        self, ifd_start: int, num_entries: int, tiff_header_offset: int, endianness: str
    ) -> dict:
        """
        Parses and reads the IFD Image File Directory (IFD) and extracts its related tags.
        The same goes for the other IFD parser methods below.

        This method reads the IFD, identifies its entries, and extracts metadata tags.

        :param ifd_start: The absolute offset where the IFD starts.
        :type ifd_start: int
        :param num_entries: The number of directory entries in the IFD.
        :type num_entries: int
        :param tiff_header_offset: The offset of the TIFF header within the EXIF data.
        :type tiff_header_offset: int
        :param endianness: The byte order used for reading the EXIF metadata (">" for big-endian, "<" for little-endian).
        :type endianness: str

        :return: A dictionary containing extracted EXIF tags and their values.
        :rtype: dict
        """

        first_ifd_info = {
            "Offset to EXIF IFD": False,
            "Number of EXIF Entries": False,
            "Offset to GPS IFD": False,
            "Number of GPS Entries": False,
            "Offset to 1st IFD": False,
            "Number of 1st IFD Entries": False,
        }
        tiff_data = {}

        # This loop starts at the recorded start of the first ifd,
        # skips the 2 num_entries bytes, and iterates over each entry.
        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry * 12)
            tag, datatype, count, value = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )
            tag_bytes = tag.to_bytes(
                2, byteorder="big"
            )  # Convert integer tag to byte format

            if tag_bytes == EXIF_IFD_POINTERS["exif_ifd_pointer"]:  # Exif IFD Pointer
                exif_ifd_offset = tiff_header_offset + value
                num_exif_entries = struct.unpack(
                    f"{endianness}H",
                    self._APP1_SEGMENT[exif_ifd_offset : exif_ifd_offset + 2],
                )[0]
                first_ifd_info["Offset to EXIF IFD"] = exif_ifd_offset
                first_ifd_info["Number of EXIF Entries"] = num_exif_entries

            if tag_bytes == EXIF_IFD_POINTERS["gps_ifd_pointer"]:
                gps_ifd_offset = tiff_header_offset + value
                num_gps_entries = struct.unpack(
                    f"{endianness}H",
                    self._APP1_SEGMENT[gps_ifd_offset : gps_ifd_offset + 2],
                )[0]

                first_ifd_info["Offset to GPS IFD"] = gps_ifd_offset
                first_ifd_info["Number of GPS Entries"] = num_gps_entries

            if tag_bytes in TIFF_TAG_DICT_REV:
                tag_name = TIFF_TAG_DICT_REV[tag_bytes]

            if tag_bytes not in TIFF_TAG_DICT_REV:
                tag_name = f"Unknown_{repr(tag_bytes)}"

            tiff_data[tag_name] = self._parse_tag(
                tag=tag,
                data_type=datatype,
                count=count,
                value=value,
                entry_offset=entry_offset,
                tiff_offset=tiff_header_offset,
                endianness=endianness,
                order=entry,
            )

        next_ifd_pointer_offset = ifd_start + 2 + (12 * num_entries)

        if next_ifd_pointer_offset + 4 <= len(self._APP1_SEGMENT):
            next_ifd_pointer_bytes = self._APP1_SEGMENT[
                next_ifd_pointer_offset : next_ifd_pointer_offset + 4
            ]

            next_ifd_offset_relative = struct.unpack(
                f"{endianness}I", next_ifd_pointer_bytes
            )[0]

            if next_ifd_offset_relative != 0:
                next_ifd_offset_absolute = tiff_header_offset + next_ifd_offset_relative

                if next_ifd_offset_absolute + 2 <= len(self._APP1_SEGMENT):
                    num_next_ifd_entries = struct.unpack(
                        f"{endianness}H",
                        self._APP1_SEGMENT[
                            next_ifd_offset_absolute : next_ifd_offset_absolute + 2
                        ],
                    )[0]
                    first_ifd_info["Offset to 1st IFD"] = next_ifd_offset_absolute
                    first_ifd_info["Number of 1st IFD Entries"] = num_next_ifd_entries
                else:
                    print(
                        f"[WARN] 1st IFD pointer out of bounds: {next_ifd_offset_absolute}"
                    )
        else:
            print(
                "[WARN] Could not read 1st IFD pointer from offset {next_ifd_pointer_offset}"
            )
        return (
            first_ifd_info,
            tiff_data,
        )

    def _read_thumbnail_ifd(
        self, ifd_start: int, num_entries: int, tiff_header_offset: int, endianness: str
    ) -> dict:
        thumbnail_ifd_tags = {}

        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry * 12)

            tag, datatype, count, value = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )
            tag_bytes = tag.to_bytes(
                2, byteorder="big"
            )  # Convert integer tag to byte format

            tag_name = TIFF_TAG_DICT_REV.get(tag_bytes, f"Unknown_{repr(tag_bytes)}")
            # if tag_name.startswith("Unknown"):
            #     pass

            thumbnail_ifd_tags[tag_name] = self._parse_tag(
                tag=tag,
                data_type=datatype,
                count=count,
                value=value,
                entry_offset=entry_offset,
                tiff_offset=tiff_header_offset,
                endianness=endianness,
                order=entry,
            )

        return thumbnail_ifd_tags

    def _read_exif_ifd(
        self, ifd_start: int, num_entries: int, tiff_header_offset: int, endianness: str
    ) -> dict:

        # Extract key EXIF tags
        exif_ifd_information = {
            "Offset to Interop IFD": False,
            "Number of Interop Entries": False,
        }
        exif_data = {}

        # Iterate over the Exif specific IFD entries
        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry * 12)  # Rec
            tag, datatype, count, value = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )

            tag_bytes = tag.to_bytes(
                2, byteorder="big"
            )  # Convert integer tag to byte format

            # Parses EXIF tags
            if tag_bytes == EXIF_IFD_POINTERS["interoperability_ifd_pointer"]:
                interop_offset = tiff_header_offset + value
                num_interop_entries = struct.unpack(
                    f"{endianness}H",
                    self._APP1_SEGMENT[interop_offset : interop_offset + 2],
                )[0]
                exif_ifd_information["Offset to Interop IFD"] = interop_offset
                exif_ifd_information["Number of Interop Entries"] = num_interop_entries

            if tag_bytes in EXIF_TAG_DICT_REV:
                tag_name = EXIF_TAG_DICT_REV[tag_bytes]

            # Parses unknown tags to adhere future improvements
            if tag_bytes not in EXIF_TAG_DICT_REV:
                tag_name = f"Unknown_{repr(tag_bytes)}"

            exif_data[tag_name] = self._parse_tag(
                tag=tag,
                data_type=datatype,
                count=count,
                value=value,
                entry_offset=entry_offset,
                tiff_offset=tiff_header_offset,
                endianness=endianness,
                order=entry,
            )

        return exif_ifd_information, exif_data

    def _read_gps_ifd(
        self, ifd_start: int, num_entries: int, tiff_header_offset: int, endianness: str
    ) -> dict:

        # Extract key gps tags
        gps_data = {}

        # Iterate over the GPS specific IFD entries
        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry * 12)  # Rec
            tag, datatype, count, value = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )

            tag_bytes = tag.to_bytes(
                2, byteorder="big"
            )  # Convert integer tag to byte format

            # Parses EXIF tags
            tag_name = GPS_TAG_DICT_REV.get(tag_bytes, f"Unknown_{repr(tag_bytes)}")
            # if tag_name.startswith("Unknown"):
            #     pass

            gps_data[tag_name] = self._parse_tag(
                tag=tag,
                data_type=datatype,
                count=count,
                value=value,
                entry_offset=entry_offset,
                tiff_offset=tiff_header_offset,
                endianness=endianness,
                order=entry,
            )

        return gps_data

    def _read_interop_ifd(
        self, ifd_start: int, num_entries: int, tiff_header_offset: int, endianness: str
    ) -> dict:

        # Extract key gps tags
        interop_data = {}

        # Iterate over the GPS specific IFD entries
        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry * 12)  # Rec
            tag, datatype, count, value = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )

            tag_bytes = tag.to_bytes(
                2, byteorder="big"
            )  # Convert integer tag to byte format

            # Parses EXIF tags
            tag_name = INTEROP_TAG_DICT_REV.get(tag_bytes, f"Unknown_{repr(tag_bytes)}")
            # if tag_name.startswith("Unknown"):
            #     pass

            interop_data[tag_name] = self._parse_tag(
                tag=tag,
                data_type=datatype,
                count=count,
                value=value,
                entry_offset=entry_offset,
                tiff_offset=tiff_header_offset,
                endianness=endianness,
                order=entry,
            )

        return interop_data

    def _parse_tag(
        self,
        tag: bytes,
        data_type: int,
        count: int,
        value: int,
        entry_offset: int,
        tiff_offset: int,
        endianness: str,
        order: int,
    ) -> dict:
        """
        Parses an identified EXIF tag within the `_read_ifd()` method, ensuring that
        the tag is processed according to its byte size and recorded data type.

        If the tag's value field exceeds 4 bytes, the function retrieves the value
        from the appropriate offset in the APP1 segment.

        :param tag: The tag identifier in bytes.
        :type tag: bytes

        :param data_type: The numeric representation of the tag’s data type.
        :type data_type: int

        :param count: The number of data values associated with the tag.
        :type count: int

        :param value: The recorded value of the tag (or an offset if the value is stored elsewhere).
        :type value: int

        :param entry_offset: The absolute offset of the tag entry within the EXIF data.
        :type entry_offset: int

        :param tiff_offset: The TIFF header offset used for relative positioning.
        :type tiff_offset: int

        :param endianness: The endianness of the EXIF data ('<' for little-endian, '>' for big-endian).
        :type endianness: str

        :param order: The order of the tag within the parsed EXIF structure.
        :type order: int

        :return: A dictionary containing detailed tag information. If the tag’s value exceeds 4 bytes,
                 the content is extracted from the APP1 segment.
        :rtype: dict
        """

        type_name = TAG_TYPES.get(
            data_type, "UNDEFINED"
        )  # Fetches type UNDEFINED if fails
        doc_type = self._get_tag_type(tag=tag, endianness=endianness)
        doc_count = self._get_tag_count(tag=tag, endianness=endianness)

        size_of_type = TAG_TYPE_SIZE_BYTES.get(type_name, 1)
        total_data_length = count * size_of_type
        absolute_offset = value + tiff_offset + self.marker_info["APP1"]["offset"]

        is_overflow = total_data_length > 4 or type_name in OVERFLOW_TYPES
        # is_big = int(value) > 1024

        if is_overflow:
            content_bytes = self._APP1_SEGMENT[
                value + tiff_offset : value + tiff_offset + total_data_length
            ]
            content_offset = value
            if total_data_length > 50:
                value = f"Deferred @ abs offset: {absolute_offset}"
            elif type_name in RATIONAL_TYPES:
                value = self._parse_rational(content_bytes, endianness)
            elif type_name in ["ASCII", "UTF-8"]:
                try:
                    value = content_bytes.split(b"\x00", 1)[0].decode(
                        "utf-8", errors="replace"
                    )
                except Exception:
                    value = content_bytes.hex()
            elif type_name == "UNDEFINED":
                value = content_bytes.hex()
            elif type_name == "FLOAT":
                value = struct.unpack(f"{endianness}f", content_bytes[:4])[0]
            elif type_name == "DOUBLE":
                value = struct.unpack(f"{endianness}d", content_bytes[:8])[0]
            else:
                value = int.from_bytes(content_bytes[:4], endianness)

            return {
                "Markup": f"[{entry_offset}:{entry_offset+12}]",
                "Absolute Offset": entry_offset,
                "TIFF Offset": entry_offset - tiff_offset,
                "Recorded Type": data_type,
                "Type": type_name,
                "Expected Type": doc_type,
                "Count": count,
                "Expected Count": doc_count,
                "Value Field Points To": absolute_offset,
                "Content Bytes": content_offset,
                "Content Value": value,
                "IFD Tag Order": order,
            }

        inline_bytes = value.to_bytes(
            4, byteorder="little" if endianness == "<" else "big"
        )
        byteorder_str = "little" if endianness == "<" else "big"

        if type_name in ["ASCII", "UTF-8"]:
            try:
                decoded = inline_bytes.split(b"\x00", 1)[0].decode(
                    "utf-8", errors="replace"
                )
            except Exception:
                decoded = inline_bytes.hex()
            content_value = decoded
        elif type_name in RATIONAL_TYPES:
            content_value = self._parse_rational(inline_bytes, endianness)
        elif type_name == "FLOAT":
            content_value = struct.unpack(f"{endianness}f", inline_bytes[:4])[0]
        else:
            content_value = int.from_bytes(inline_bytes[:4], byteorder_str)

        return {
            "Markup": f"[{entry_offset}:{entry_offset+12}]",
            "Absolute Offset": entry_offset,
            "TIFF Offset": entry_offset - tiff_offset,
            "Recorded Type": data_type,
            "Type": type_name,
            "Expected Type": doc_type,
            "Count": count,
            "Expected Count": doc_count,
            "Content Bytes": inline_bytes.hex(),
            "Content Value": content_value,
            "IFD Tag Order": order,
        }

    def _read_iptc_data(self, app13_bytes: bytes) -> dict:
        """
        Parses IPTC metadata from the APP13 segment and returns structured tag info.
        """
        iptc_data = {}
        pos = 0
        tag_order = 0

        try:
            while pos < len(app13_bytes):
                if app13_bytes[pos : pos + 13] == b"Photoshop 3.0\x00":
                    pos += 13
                    continue

                if app13_bytes[pos : pos + 4] == b"8BIM":
                    resource_id = int.from_bytes(app13_bytes[pos + 4 : pos + 6], "big")
                    name_len = app13_bytes[pos + 6]
                    name_pad = 1 if name_len % 2 == 0 else 0
                    size_start = pos + 6 + 1 + name_len + name_pad
                    size = int.from_bytes(
                        app13_bytes[size_start : size_start + 4], "big"
                    )
                    data_start = size_start + 4
                    data_end = data_start + size

                    if resource_id == 0x0404:
                        iptc_block = app13_bytes[data_start:data_end]
                        iptc_data.update(
                            self._parse_iptc_fields(iptc_block, data_start, tag_order)
                        )
                    pos = data_end + (size % 2)
                else:
                    pos += 1
        except Exception as e:
            iptc_data = {"[ERROR]": f"Failed to parse APP13 segment: {e}"}

        return iptc_data

    def _parse_iptc_fields(
        self, iptc_block: bytes, offset_start: int, tag_order: int
    ) -> dict:
        result = {}
        pos = 0

        while pos < len(iptc_block):
            if iptc_block[pos] == 0x1C:
                record = iptc_block[pos + 1]
                tag = iptc_block[pos + 2]
                length = int.from_bytes(iptc_block[pos + 3 : pos + 5], "big")
                value_bytes = iptc_block[pos + 5 : pos + 5 + length]

                tag_name = next(
                    (
                        name
                        for name, props in IPTC_TAGS.items()
                        if props["tag"] == tag and props.get("record", record) == record
                    ),
                    f"Unknown_{record}_{tag}",
                )
                absolute_offset = offset_start + pos
                try:
                    value = value_bytes.decode("utf-8", errors="replace")
                except Exception:
                    value = value_bytes.hex()

                result[tag_name] = {
                    "Absolute Offset": absolute_offset,
                    "Content Bytes": repr(value_bytes),
                    "Content Value": value,
                    "Length": length,
                    "Tag Order": tag_order,
                }

                tag_order += 1
                pos += 5 + length
            else:
                pos += 1

        return result

    def _get_tag_type(self, tag: bytes, endianness: str) -> str:
        """
        Given a tag ID (in bytes) and endianness ('MM' = Big-Endian, 'II' = Little-Endian),
        returns the corresponding EXIF tag type from the TAG_TYPES dictionary.

        :param tag_bytes: The raw tag ID (e.g., b'\x90\x03').
        :type tag_bytes: bytes

        :return: The tag type (e.g., "ASCII", "RATIONAL") or None if not found.
        :rtype: str
        """
        if endianness == "<":
            tag_bytes = struct.pack(f">H", tag)  # Packs as
        elif endianness == ">":
            tag_bytes = struct.pack(f"{endianness}H", tag)

        tag_name = ALL_TAGS_REV.get(tag_bytes)

        if tag_name:
            tag_info = ALL_TAGS.get(tag_name)
            return tag_info["type"]

    def _get_tag_count(self, tag: bytes, endianness: str) -> str:
        """
        Given a tag ID (in bytes) and endianness ('MM' = Big-Endian, 'II' = Little-Endian),
        returns the corresponding EXIF count from the TAG_TYPES dictionary.

        :param tag_bytes: The raw tag ID (e.g., b'\x90\x03').
        :type tag_bytes: bytes

        :return: The tag type (e.g., "ASCII", "RATIONAL") or None if not found.
        :rtype: str
        """
        if endianness == "<":
            tag_bytes = struct.pack(f">H", tag)
        elif endianness == ">":
            tag_bytes = struct.pack(f"{endianness}H", tag)

        tag_name = ALL_TAGS_REV.get(tag_bytes)

        if tag_name:
            tag_info = ALL_TAGS.get(tag_name)
            return tag_info["count"]

    def _parse_rational(
        self, content_bytes: bytes, endianness
    ) -> str | int:  # "<" for little-endian, ">" for big-endian
        """
        Parses a rational number (numerator/denominator) from EXIF metadata.

        Rational values in EXIF metadata are typically stored as two 4-byte integers with a numerator (num) and adenominator (denom).

        This function correctly unpacks these values according to the specified byte order.

        :param content_bytes: The 8-byte content representing the rational value.
        :type content_bytes: bytes

        :param endianness: The byte order to use for unpacking ('<' for little-endian, '>' for big-endian).
        :type endianness: str


        :return: A tuple containing a string representation of a fraction and a decimal value of the fraction
        :rtype: tuple
        """
        if len(content_bytes) < 8:
            return None
        try:
            num, denom = struct.unpack(f"{endianness}II", content_bytes)
            fraction_str = (
                f"{num}/{denom}" if denom else f"{num}/1"
            )  # Avoid division by zero
            # decimal_value = num / denom if denom else num  # Compute decimal representation
            return fraction_str
        except Exception as e:
            print(f"[WARN] Failed to unpack rational value: {e}")
            return None

    def get_exif_image_data(self) -> dict:
        """
        Extracts and returns EXIF metadata from the image.

        This method scans the JPEG file for EXIF data within the APP1 segment and
        returns a structured metadata report.

        :return: A dictionary containing:
            - **File Name**: self.img_path
            - **EXIF Info** (*dict*): The information located within the file APP1 section emphasizing EXIF information.
        :rtype: dict

        """

        # Extract JPEG markers

        jpeg_marker_info = self._read_jpeg_markers()
        self.marker_info = jpeg_marker_info
        app1_info = {"[ERROR]": "No APP1 segment found."}
        # iptc_info = {"[INFO]": "No IPTC data found."}

        # General File Info
        _, file_ext = os.path.splitext(self.img_path)
        file_size = len(self.binary_repr)

        general_info = {
            "file_name": os.path.basename(self.img_path),
            "file_format": file_ext,
            "file_size_bytes": f"{file_size} bytes",
            "file_size_kbytes": f"{round(file_size / 1024, 2)} kbs",
        }

        # Parse APP1 (EXIF) if present
        if "APP1" in jpeg_marker_info:
            try:
                app1_info = self._read_app1_segment(jpeg_marker_info["APP1"]["offset"])
                self.app1_data = app1_info
            except Exception as e:
                app1_info = {"[ERROR]": f"Failed to parse APP1 segment: {e}"}

        output = {
            "APP1 Info": app1_info,
        }

        return output

    def get_complete_image_data(self) -> dict:
        """
        Extracts and returns a complete metadata report for the image.

        This method extracts general file information, JPEG markers, and metadata
        from the APP1 segment.

        :return: A dictionary containing:
            - **General File Info** (*dict*): File name, format, and size details.
            - **jpeg_markers** (*dict*): Extracted JPEG markers.
            - **APP1 Info** (*dict*): Parsed metadata from the APP1 segment.
        :rtype: dict
        """
        # Extract JPEG markers
        jpeg_marker_info = self._read_jpeg_markers()
        self.marker_info = jpeg_marker_info

        # Prepare default APP1 response
        # Extract APP1 segment and EXIF data
        if "APP1" not in jpeg_marker_info:
            app1_info = {"error": "No APP1 segment found in the image."}
        elif "APP1" in jpeg_marker_info:
            app1_info = self._read_app1_segment(jpeg_marker_info["APP1"]["offset"])
            self.app1_data = app1_info

        # Parse APP13 if present
        if "APP13" in jpeg_marker_info:
            app13_offset = jpeg_marker_info["APP13"]["offset"]
            app13_size = jpeg_marker_info["APP13"]["size"]
            app13_bytes = self.binary_repr[
                app13_offset + 4 : app13_offset + 2 + app13_size
            ]
            iptc_data = self._read_iptc_data(app13_bytes)

            self._APP13_SEGMENT = self.binary_repr[
                app13_offset : app13_offset + app13_size
            ]

        else:
            iptc_data = False

        # Construct full report
        _, file_ext = os.path.splitext(self.img_path)
        file_size = len(self.binary_repr)

        output = {
            "General File Info": {
                "file_name": os.path.basename(self.img_path),
                "file_format": file_ext,
                "file_size_bytes": f"{file_size} bytes",
                "file_size_kbytes": f"{round(file_size/1024, 2)} kbs",
            },
            "JPEG Marker Segments": jpeg_marker_info,
            "APP1 Info": app1_info,
        }

        if iptc_data:
            output.update({"IPTC Info": iptc_data})

        self.file_data = output
        return output

    @classmethod
    def get_image_datas(
        cls,
        images: str | list["JPEGParser"],
        verbose: str = "complete",
        limit: int = None,
        segment: tuple[int, int] = None,
    ) -> list[dict]:
        """
        Generates metadata reports for all images in a given folder.
        NOTE: For single image data retrieval, please use get_exif_image_data() or get_complete_image_data().

        This method scans the provided folder for JPEG images and extracts metadata
        based on the specified verbosity level.

        :param folder_path: The path to the folder containing images.
        :type folder_path: str

        :param verbose: Specifies the level of metadata extraction. Options:
            - complete (default): Extracts full metadata, fetches get_complete_image_data().
            - exif: Extracts only EXIF metadata, fetches get_exif_image_data().
        :type verbose: str, optional

        :param limit: Defines the portion of the folder you wish to fetch.
        :type limit: int

        :param segment: Defines a segment of the folder you wish to fetch.
        :type segmnet: tuple(int, int)

        :return: A list of dictionaries, where each dictionary contains metadata for an image.
        :rtype: list[dict]
        """
        if isinstance(images, str):
            if not os.path.isdir(images):
                raise ValueError("Invalid folder path.")

            # Get all JPEG images from a folder
            all_files = os.listdir(images)
            image_files = [
                os.path.join(images, f)
                for f in all_files
                if os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
            ]

            skipped = len(all_files) - len(image_files)
            if skipped:
                print(f"[INFO] Skipped {skipped} non-JPEG files in '{images}'")

            if not image_files:
                return []

            if not image_files:
                raise ValueError("No valid images found in the folder.")

        elif isinstance(images, list):
            image_files = images  # already JPEGParser instances
        else:
            raise TypeError(
                "images must be either a folder path or a list of JPEGParser instances."
            )

        if segment:
            start, end = segment
            image_files = image_files[start:end]

        if limit is not None:
            image_files = image_files[:limit]

        return cls._verbosed_output(image_files, verbose=verbose)

    @classmethod
    def _verbosed_output(cls, image_files: list, verbose: str) -> list[dict]:
        """ute
        Helper method for get_image_datas(). Always includes conformity metrics.

        :param image_files: List of JPEGParser objects or image paths.
        :param verbose: Either "complete" or "exif".
        :param metrics: Ignored now, always True.
        :return: List of dictionaries with filename, metadata, and conformity metrics.
        """
        if not image_files:
            return []

        if isinstance(image_files[0], str):
            image_objects = [cls(img) for img in image_files]
        else:
            image_objects = image_files

        if verbose == "complete":
            return [
                {
                    "file_name": os.path.basename(img.img_path),
                    "data": img.get_complete_image_data(),
                }
                for img in image_objects
            ]

        elif verbose == "exif":
            return [
                {
                    "file_name": os.path.basename(img.img_path),
                    "data": img.get_exif_image_data(),
                }
                for img in image_objects
            ]
        else:
            raise ValueError(f"Invalid verbose option: '{verbose}'")

    def _get_tag_id(self, tag_name: str) -> bytes | None:
        if tag_name.lower() == "unknown":
            return None
        tag_info = ALL_EXIF_TAGS.get(tag_name)
        return tag_info["tag"] if tag_info else None

    def _get_support_level(self, tag_name: str, mode: str = "compressed") -> str:
        """
        Return the support level letter ('M', 'O', 'R', etc.) for the given tag and mode.
        Defaults to 'compressed' mode. Returns 'U' if unknown.
        """
        tag_info = ALL_SUPPORT_LEVELS.get(tag_name)
        if not tag_info or "support" not in tag_info:
            return "U"

        support_data = tag_info["support"]

        # Handle compressed directly, or dig into uncompressed formats
        if mode == "compressed":
            return support_data.get("compressed", "U")
        elif mode in {"chunky", "planar", "ycc"}:
            return support_data.get("uncompressed", {}).get(mode, "U")
        else:
            return "U"

    def _sort_by_byte(self, tag_dict: dict) -> list[bytes]:
        """
        Sorts the byte keys of a reversed tag dictionary (e.g. EXIF_TAG_DICT_REV).
        Returns the keys sorted by their integer value (ascending).
        """
        return sorted(tag_dict.keys(), key=lambda b: int.from_bytes(b, byteorder="big"))

    def compute_conformity_metrics(self):
        """
        Computes conformity metrics (ECS, H, TVS, TOS) based on parsed EXIF data.
        Stores the results as attributes on the JPEGParser object.
        """
        if not self.app1_data:
            raise ValueError(
                "APP1 metadata not found. Run `get_complete_image_data()` first."
            )

        # Baseline lists for comparison scoring
        baseline_exif = self._sort_by_byte(EXIF_TAG_DICT_REV)
        baseline_gps = self._sort_by_byte(GPS_TAG_DICT_REV)
        baseline_interop = self._sort_by_byte(INTEROP_TAG_DICT_REV)

        # Header Validity Score
        e = int(bool(self.app1_data.get("EXIF Identifier Offset", False)))
        t = int(bool(self.app1_data.get("TIFF Magic Number Offset", False)))
        b = int(bool(self.app1_data.get("Byte Order", None)))

        header_score = calculate_header_validity(e, t, b)
        self.header_validity_score = header_score

        all_tag_dicts = []
        observed_exif, observed_gps, observed_interop = [], [], []

        # Iterate over IFDs
        ifds = [
            ("EXIF", self.exif_ifd_data, baseline_exif, observed_exif),
            ("GPS", self.gps_ifd_data, baseline_gps, observed_gps),
            ("Interop", self.interop_ifd_data, baseline_interop, observed_interop),
        ]

        for ifd_name, ifd_data, baseline, observed in ifds:
            if ifd_data:
                for tag_name, tag_data in ifd_data.items():
                    tag_id = self._get_tag_id(tag_name)
                    tag_info = {
                        "name": tag_name,
                        "tag_id": tag_id,
                        "type_valid": tag_data.get("Type") == tag_data.get("Doc Type"),
                        "count_valid": (
                            tag_data.get("Doc Count") == "Any"
                            or tag_data.get("Count") == tag_data.get("Doc Count")
                        ),
                        "present": True,
                        "support_level": self._get_support_level(tag_name),
                        "order": tag_data.get("Tag Order", 0),
                    }
                    if tag_id:
                        observed.append(tag_id)
                    all_tag_dicts.append(tag_info)

        # Tag Validity Score
        tag_validity_score = calculate_tag_validity_score(all_tag_dicts)

        # Calculate TOS
        weak_tos_scores = {}
        strict_tos_scores = {}
        weak_tag_order_scores = []
        strict_tag_order_scores = []

        if observed_exif:
            exif_tag_dicts = [
                tag for tag in all_tag_dicts if tag["tag_id"] in observed_exif
            ]
            weak_tos_scores["EXIF"] = round(
                calculate_strict_TOS(observed_exif, baseline_exif), 5
            )
            strict_tos_scores["EXIF"] = round(
                calculate_lazy_TOS(exif_tag_dicts, baseline_exif), 5
            )

            strict_tag_order_scores.append(strict_tos_scores["EXIF"])
            weak_tag_order_scores.append(weak_tos_scores["EXIF"])

        if observed_gps:
            gps_tag_dicts = [
                tag for tag in all_tag_dicts if tag["tag_id"] in observed_gps
            ]
            weak_tos_scores["GPS"] = round(
                calculate_strict_TOS(observed_gps, baseline_gps), 5
            )
            strict_tos_scores["GPS"] = round(
                calculate_lazy_TOS(gps_tag_dicts, baseline_gps), 5
            )

            strict_tag_order_scores.append(strict_tos_scores["EXIF"])
            weak_tag_order_scores.append(weak_tos_scores["EXIF"])

        if observed_interop:
            interop_tag_dicts = [
                tag for tag in all_tag_dicts if tag["tag_id"] in observed_interop
            ]
            weak_tos_scores["Interop"] = round(
                calculate_strict_TOS(observed_interop, baseline_interop), 5
            )
            strict_tos_scores["Interop"] = round(
                calculate_lazy_TOS(interop_tag_dicts, baseline_interop), 5
            )

            strict_tag_order_scores.append(strict_tos_scores["EXIF"])
            weak_tag_order_scores.append(weak_tos_scores["EXIF"])
        # Final tag order score (average of available TOS)
        weak_tag_order = (
            round(sum(weak_tag_order_scores) / len(weak_tag_order_scores), 5)
            if weak_tag_order_scores
            else 0.0
        )
        strict_tag_order = (
            round(sum(strict_tag_order_scores) / len(strict_tag_order_scores), 5)
            if strict_tag_order_scores
            else 0.0
        )

        # EXIF Conformity Score
        ecs = round(calculate_ECS(header_score, tag_validity_score, weak_tag_order), 5)

        self.header_validity_score = header_score
        self.tag_validity_score = tag_validity_score
        self.weak_tag_order_score = weak_tos_scores
        self.strict_tag_order_score = strict_tag_order
        self.ecs = ecs
        return {
            "Header VAL": round(header_score, 5),
            "Tag VAL Score": round(tag_validity_score, 5),
            "Lazy Tag Order Score": strict_tos_scores,
            "Strict Tag Order Score": weak_tos_scores,
            "EXIF Conformity Score": ecs,
        }

    @staticmethod
    def pretty_print(data: dict):
        """
        Pretty-print a metadata dictionary using Rich.

        Args:
            data (dict): The dictionary to pretty-print.

        Raises:
            ValueError: If the input is not a dict or is empty.
        """
        if not isinstance(data, dict):
            raise ValueError("Input to pretty_print_dict must be a dictionary.")
        if not data:
            raise ValueError("Cannot pretty print an empty dictionary.")
        rich_print(data)


# if __name__ == "__main__":

# path = r"D:\image_dataset\Images\Dresden_image_dataset\Agfa_DC-504_0\Agfa_DC-504_0_1.JPG"
# img = JPEGParser(path)
# print(img.binary_repr[406:450])
# print(img.get_complete_image_data())
