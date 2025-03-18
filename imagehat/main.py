import os
import os.path
import struct
from identifiers.constants import (
    MARKER_SEGMENTS_JPEG_ADDRESS,
    MARKER_SEGMENTS_JPEG_NAME,
    IDENTIFIERS,
)
from identifiers.tag_support_levels import (
    TAG_TYPES,
    OVERFLOW_TYPES,
    EXIF_TAGS,
    EXIF_GPS_TAGS,
    EXIF_TAG_DICT_REV,
    GPS_TAG_DICT_REV,
)
from identifiers.valid_formats import VALID_FORMATS


class ImageHat:
    """
    The JPEGParser class is a sub class of the ImageHat super class. It is designed to analyze binary image files and
    extract EXIF metadata directly from from binary image files. It supports methods for parsing JPEG, extracting EXIF
    data, and - most importantly - converting raw bytes represented as hexadecimals in order to parse structured information
    from bytes.

    Example Usage:
    --------------
    >>> image = ImageHat("sample.jpg")
    >>> markers = image.get_image_data(verbose="exif")
    >>> print(markers)
    """

    def __init__(self, img_path):
        self.img_path: str = img_path
        self._validate_file_path()
        self.binary_repr: bytes = (
            self.get_binary_data()
        )  # creates hexadecimal representaion
        self._APP1_SEGMENT = None
        self.file_info: None | dict = None
        self.app1_info: None | dict = None
        self.exif_info: None | dict = None

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
        if ext.lower() not in {".jpg", ".jpeg"}:
            raise ValueError(
                f"Invalid file format '{ext}'. Supported formats: .jpg, .jpeg."
            )

        try:
            with open(self.img_path, "rb") as f:
                header = f.read(2)
                if (
                    header != MARKER_SEGMENTS_JPEG_NAME["SOI"]
                ):  # JPEG files start with 0xFFD8
                    raise ValueError("File is not a valid JPEG (missing SOI marker).")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {e}") from e

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

    def __str__(self) -> str:
        """
        Method used to show basic information the ImageHat object.
        """
        return f"ImageHat: {self.img_path}, Size: {len(self.binary_repr)} bytes"

    def segment_data(self, end: int, start: int | None = None) -> None:
        """
        Metod for printing the whole byte array. Should be avoided as printed byte arrays are living nightmares.

        :return: a segment of self.binary_repr
        """
        if start is None:
            return self.binary_repr[:end]
        return self.binary_repr[start:end]

    def _read_jpeg_markers(self) -> dict[int | list[int]]:
        """
        Identifies and extracts key JPEG markers in the binary image.

        This method scans the binary representation of the image to locate JPEG markers,
        count their occurrences, and determine their byte offsets. Currently, it is limited
        to finding only the **first** occurrence of each marker, as overlapping markers
        make deeper analysis challenging

        .. note::
            Due to the complexity of marker placement in JPEG images, this method does not
            guarantee the extraction of all markers if multiple overlapping occurences exist.
            As they usually do.

        :return: A dictionary where keys represent marker names, and values contain marker-specific
                 metadata, including occurrence count and byte offsets.
        :rtype: dict

        """
        marker_info = {}

        for marker, name in MARKER_SEGMENTS_JPEG_ADDRESS.items():
            offset = []
            pos = self.binary_repr.find(marker)  # Find first occurrence

            while pos != -1:
                offset.append(pos)
                pos = self.binary_repr.find(marker, pos + 1)  # Find next occurrence

            if offset:  # Only store markers that were found
                marker_info[name] = {"count": len(offset), "offset": offset}
        return marker_info

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
        report = {}
        # Recording APP1 segment size (s.b. 2 bytes)
        app1_size = int.from_bytes(
            self.binary_repr[app1_offset + 2 : app1_offset + 4], byteorder="big"
        )

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

        # Recording EXIF identifier (s.b. 4 bytes, 6 bytes including padding)
        exif_identifier = self._APP1_SEGMENT.find(IDENTIFIERS["exif_identifier"])
        report["EXIF Identifier Offset"] = exif_identifier if exif_identifier else None

        # Recording byte order (should be 2 bytes)
        # Recodring endianness starts here. EXIF is big-endian until byte-order is discovered.
        byte_order_offset, endianness_report = self._find_target_byte(
            self._APP1_SEGMENT[:25], targets=[IDENTIFIERS["II"], IDENTIFIERS["MM"]]
        )
        byte_order_bytes = self._APP1_SEGMENT[byte_order_offset : byte_order_offset + 2]

        # Setting endianness for the rest of runtime
        endianness = "<" if byte_order_bytes == IDENTIFIERS["II"] else ">"
        report["Byte Order"] = endianness_report

        # Recording magic number (s.b. 2 bytes)
        magic_number = self._convert_internal_identifier(
            endianness, "H", "tiff_magic_number"
        )
        magic_number_offset = self._APP1_SEGMENT.find(magic_number)

        magic_number_bytes = self._APP1_SEGMENT[
            magic_number_offset : magic_number_offset + 2
        ]  # Read raw bytes
        magic_number = struct.unpack(f"{endianness}H", magic_number_bytes)[0]
        report["TIFF Magic Number"] = magic_number_bytes
        report["TIFF Magic Number Offset"] = magic_number_offset

        ### Extremely important NOTE. All markers and tags in the JEITA documentations are displayed in MSB.
        ### Always unpack constants in big endian from project files.
        comp_magic_number = struct.unpack(">H", IDENTIFIERS["tiff_magic_number"])[0]
        report["TIFF Validity"] = magic_number == comp_magic_number

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
        report["0th IFD bytes"] = ifd_offset_bytes
        report["0th IFD offset"] = ifd_offset
        report["0th IFD start"] = ifd_start
        report["Entries in 0th IFD"] = ifd_entries

        # Recording the EXIF tags. NOTE: Most important, do not touch.
        exif_information = self._read_exif_ifd(
            ifd_start=ifd_start,
            num_entries=ifd_entries,
            tiff_header_offset=byte_order_offset,
            endianness=endianness,
        )
        report["EXIF Info"] = exif_information

        return report

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
        return None

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

    def _read_exif_ifd(
        self, ifd_start: int, num_entries: int, tiff_header_offset: int, endianness: str
    ) -> dict:
        """
        Parses and reads the identified argumented Image File Directory (IFD) and extracts its related tags.

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
        report = {}

        # This loop starts at the recorded start of the first ifd,
        # skips the 2 num_entries bytes, and iterates over each entry.
        exif_ifd_offset = None
        for entry in range(num_entries):
            entry_offset = ifd_start + 2 + (entry * 12)
            tag, datatype, count, value_offset = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )
            hex_tag = tag.to_bytes(2, "big")
            if hex_tag == IDENTIFIERS["exif_ifd_pointer"]:  # Exif IFD Pointer
                exif_ifd_offset = tiff_header_offset + value_offset
                report["Exif IFD pointer found"] = bool(tag)
                break

        if not exif_ifd_offset:
            return {"Exif IFD Pointer not found"}

        # Read number of entries in Exif IFD
        num_exif_entries = struct.unpack(
            f"{endianness}H", self._APP1_SEGMENT[exif_ifd_offset : exif_ifd_offset + 2]
        )[0]
        report["Number of Exif Entries"] = num_exif_entries

        # Extract key EXIF tags
        exif_data = {}

        # Iterate over the Exif specific IFD entries
        for i in range(num_exif_entries):
            entry_offset = exif_ifd_offset + 2 + (i * 12)  # Rec
            tag, datatype, count, value = struct.unpack(
                f"{endianness}HHII",
                self._APP1_SEGMENT[entry_offset : entry_offset + 12],
            )

            tag_bytes = tag.to_bytes(
                2, byteorder="big"
            )  # Convert integer tag to byte format
            if tag_bytes in EXIF_TAG_DICT_REV:
                tag_name = EXIF_TAG_DICT_REV[tag_bytes]
                # if tag_name == "MakerNote": break # Just for now
                exif_data[tag_name] = self._parse_tag(
                    tag=tag,
                    data_type=datatype,
                    count=count,
                    value=value,
                    entry_offset=entry_offset,
                    tiff_offset=tiff_header_offset,
                    endianness=endianness,
                    order=i,
                )

        report["EXIF Data"] = exif_data
        return report

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
        Parses the identidified tag within the _read_ifd() and ensures that the the program
        parses the identified tags in accordance with byte size and recorded data type.

        :param data_type: represents the recorded data_type
        :type data_type: int

        :param count:
        :type count:

        :param value:
        :type value:

        :param entry_offset:
        :type entry_offset:

        :param tiff_offset:
        :type tiff_offset:

        :param endianness:
        :type endianness:

        :param order:
        :type order:

        :return: A dictionary containing frutiful tag information. Return values differs
                 if a tags' value field goes beyond 4 bytes.
        :rtype: dict
        """
        dt = TAG_TYPES.get(data_type, 7)  # Fetches type UNDEFINED if fails
        doc_type = self._get_tag_type(tag=tag, endianness=endianness)

        if dt in OVERFLOW_TYPES or count > 4:
            content_bytes = self._APP1_SEGMENT[
                value + tiff_offset : value + count + tiff_offset
            ]
            content_offset = value
            if dt in OVERFLOW_TYPES:
                content_bytes = self._APP1_SEGMENT[
                    value + tiff_offset : value + tiff_offset + 8
                ]
                value, decimal_value = self._parse_rational(content_bytes, endianness)
                # value = f"{num}/{denom}" if denom != 1 else num

            return {
                "Markup": f"[{entry_offset}:{entry_offset+12}]",
                "Absolute Offset": entry_offset,
                "TIFF offset": entry_offset - tiff_offset,
                "Recorded Type": data_type,
                "Type": dt,
                "Doc Type": doc_type,
                "Count": count,
                "Content Location": content_offset,
                "Content": bytes(content_bytes),
                "Content Value": value,
                "Tag Order": order,
                # "Status": None,  # Advanced setting, in development
            }

        return {
            "Markup": f"[{entry_offset}:{entry_offset+12}]",
            "Absolute Offset": entry_offset,
            "TIFF offset": entry_offset - tiff_offset,
            "Recorded Type": data_type,
            "Type": dt,
            "Doc Type": doc_type,
            "Count": count,
            "Content": hex(value),
            "Content Value": value,
            "Tag Order": order,
            # "Status": None,  # Advanced setting, in development
        }

    def _get_tag_type(self, tag, endianness):
        """
        Given a tag ID (in bytes) and endianness ('MM' = Big-Endian, 'II' = Little-Endian),
        returns the corresponding EXIF tag type from the TAG_TYPES dictionary.

        :param tag_bytes: The raw tag ID (e.g., b'\x90\x03').
        :type tag_bytes: bytes

        :return: The tag type (e.g., "ASCII", "RATIONAL") or None if not found.
        :rtype: str
        """
        if endianness == "<":
            tag_bytes = struct.pack(f">H", tag) # Packs as 
        elif endianness == ">":
            tag_bytes = struct.pack(f"{endianness}H", tag)

        tag_name = EXIF_TAG_DICT_REV.get(tag_bytes)

        if tag_name:
            tag_info = EXIF_TAGS.get(tag_name)
            return tag_info["type"]
        # tag_name = EXIF_TAG_DICT_REV.get(tag_bytes)
        # print(tag_name)
        # if tag_name:
        #     tag_info = EXIF_TAGS.get(tag_name) or EXIF_GPS_TAGS.get(tag_name)
        #     tag_type = tag_info["type"]
        #     return tag_type

    def _parse_rational(
        self, content_bytes, endianness
    ):  # "<" for little-endian, ">" for big-endian
        num, denom = struct.unpack(f"{endianness}II", content_bytes)
        fraction_str = (
            f"{num}/{denom}" if denom else f"{num}/1"
        )  # Avoid division by zero
        decimal_value = num / denom if denom else num  # Compute decimal representation
        return fraction_str, decimal_value  # Return both representations

    def get_image_data(self, verbose: str = None) -> dict:
        """
        Generates a thorough metadata report, including general image information.

        Args:
            verbose (str): Verbosity mode. Options:
                - "exif": Returns only EXIF metadata.

        Returns:
            dict: The metadata report based on the selected verbosity mode.
        """

        # Extract JPEG markers
        jpeg_marker_info = self._read_jpeg_markers()

        if "APP1" not in jpeg_marker_info:
            return {"error": "No APP1 segment found in the image."}

        # Extract APP1 segment and EXIF data
        app1_info = self._read_app1_segment(jpeg_marker_info["APP1"]["offset"][0])
        exif_data = app1_info.get("EXIF Info", {})

        if verbose == "exif":
            return {
                "file_name": self.img_path,
                "exif_info": exif_data,
            }  # Return only EXIF data

        # Construct full report
        _, file_ext = os.path.splitext(self.img_path)
        file_size = len(self.binary_repr)

        return {
            "General File Info": {
                "file_name": self.img_path,
                "file_format": file_ext,
                "file_size_bytes": f"{file_size} bytes",
                "file_size_kbytes": f"{round(file_size/1024, 2)} kbs",
            },
            "jpeg_markers": jpeg_marker_info,
            "APP1 Info": app1_info,
        }

    @classmethod
    def get_image_datas(cls, folder_path: str, verbose: str = None) -> list[dict]:
        """
        Generates metadata reports for all images in a folder.

        Args:
            folder_path (str): Path to the folder containing images.
            verbose (str, optional): Verbosity mode. Options:
                - None (default): Full metadata.
                - "exif": Returns only EXIF metadata.

        Returns:
            list[dict]: List of metadata reports, each corresponding to an image.
        """

        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path.")

        # Get all JPEG images
        image_files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith((".jpg", ".jpeg"))
        ]

        if not image_files:
            raise ValueError("No valid images found in the folder.")

        # Generate reports
        return [cls(img).get_image_data(verbose=verbose) for img in image_files]


if __name__ == "__main__":

    # NOTE Use the below lines to test
    # file_path_img = r"tests\testsets\testset-small\Sony_DSC_H50_Sony_DSC-H50_0_47713.JPG"
    # img = ImageHat(file_path_img)
    # meta = img_get_image_data()
    # print(meta)
    # print(meta["APP1 Info"]["EXIF Info"]["EXIF DATA"])

    # # NOTE: Testing on all camera models in Dresden Dataset
    testset_folder = os.path.join("tests", "testsets", "testset-small")
    list_of_images = [
        os.path.join(testset_folder, fp) for fp in os.listdir(testset_folder)
    ]
    images = [ImageHat(img) for img in list_of_images]

    # for i in images[8:10]:
    #     print(i.get_image_data(verbose="exif"))

    print(images[9].get_image_data())
    for i in images:
        print(i.binary_repr.find(b"\x41\x53\x43\x49\x49\x00\x00\x00"))

    # comp = ImageHat.metadata_comparison(testset_folder)
    # comp = comp.get("FocalLength")
    # for items in comp:
    #     print(items, sep=" ")
