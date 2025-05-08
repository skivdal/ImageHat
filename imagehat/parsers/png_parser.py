# imagehat/parsers/png_parser.py

import os
import zlib
import struct
from imagehat.parsers.base_parser import BaseParser
from imagehat.identifiers.extensions import VALID_EXTENSIONS
from imagehat.identifiers.png_identifiers import PNG_CHUNK_MARKERS, IDENTIFIERS

from imagehat.identifiers.exif_attribute_information import (
    TAG_TYPES,
    OVERFLOW_TYPES,
    ALL_TAGS,
    ALL_TAGS_REV,
)


class PNGParser(BaseParser):
    def __init__(self, img_path: str):
        self.img_path = img_path
        self._validate_file_path()
        self.binary_repr = self.get_binary_data()

        self.metadata = {}

    def get_binary_data(self) -> bytes:
        try:
            with open(self.img_path, "rb") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Could not read file '{self.img_path}': {e}") from e

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
        if ext.lower() not in VALID_EXTENSIONS:
            raise ValueError(f"Invalid file format '{ext}'. Supported formats: .png")

        try:
            with open(self.img_path, "rb") as f:
                header = f.read(8)  # PNG signature is 8 bytes
                if header != IDENTIFIERS["png_signature"]:
                    raise ValueError(
                        "[ERROR] Skipping file: Not a valid PNG (invalid signature)"
                    )
        except Exception as e:
            print(f"Error reading file: {e}")

    def _parse_IHDR(self, data):
        return {
            "width": int.from_bytes(data[0:4], "big"),
            "height": int.from_bytes(data[4:8], "big"),
            "bit_depth": data[8],
            "color_type": data[9],
            "compression": data[10],
            "filter": data[11],
            "interlace": data[12],
        }

    def _parse_tIME(self, data):
        return {
            "year": int.from_bytes(data[0:2], "big"),
            "month": data[2],
            "day": data[3],
            "hour": data[4],
            "minute": data[5],
            "second": data[6],
        }

    def _parse_tEXt(self, data):
        try:
            key, value = data.split(b"\x00", 1)
            self.metadata.setdefault("tEXt_entries", []).append(
                {
                    "keyword": key.decode(errors="ignore"),
                    "value": value.decode(errors="ignore"),
                }
            )
        except Exception:
            pass

    def _parse_text_chunk(self, data: bytes) -> dict:
        """
        Parses basic PNG textual chunks like tEXt/zTXt/iTXt.
        """
        try:
            parts = data.split(b"\x00", 1)
            keyword = parts[0].decode("utf-8", errors="replace")
            value = parts[1].decode("utf-8", errors="replace") if len(parts) > 1 else ""
            return {keyword: value}
        except Exception as e:
            return {"Error": f"Could not parse text chunk: {e}"}

    def _parse_pHYs(self, data: bytes) -> dict:
        try:
            x_ppu = int.from_bytes(data[0:4], "big")
            y_ppu = int.from_bytes(data[4:8], "big")
            unit = data[8]
            return {
                "pixels_per_unit_x": x_ppu,
                "pixels_per_unit_y": y_ppu,
                "unit": "meter" if unit == 1 else "unspecified",
            }
        except Exception as e:
            return {"Error": f"Failed to parse pHYs: {e}"}

    def _parse_iCCP(self, data: bytes) -> dict:
        try:
            null_pos = data.index(0)
            profile_name = data[:null_pos].decode("latin1", errors="replace")
            compression = data[null_pos + 1]
            return {
                "profile_name": profile_name,
                "compression": (
                    "deflate" if compression == 0 else f"unknown ({compression})"
                ),
            }
        except Exception as e:
            return {"Error": f"Failed to parse iCCP: {e}"}

    def _read_png_chunks(self) -> dict:
        """
        Mimics JPEG marker collection by reading all PNG chunks with offset and size.
        Now includes CRC validation.
        """
        offset = 8  # skip PNG signature
        markers = {}
        chunk_counts = {}

        while offset < len(self.binary_repr):
            try:
                length = int.from_bytes(self.binary_repr[offset : offset + 4], "big")
                chunk_type = self.binary_repr[offset + 4 : offset + 8]
                chunk_data = self.binary_repr[offset + 8 : offset + 8 + length]
                stored_crc = self.binary_repr[
                    offset + 8 + length : offset + 12 + length
                ]
                computed_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
                stored_crc_int = int.from_bytes(stored_crc, "big")

                chunk_type_str = chunk_type.decode(errors="replace")
                full_chunk_size = 4 + 4 + length + 4  # length + type + data + CRC

                count = chunk_counts.get(chunk_type_str, 0)
                name = chunk_type_str if count == 0 else f"{chunk_type_str}_{count}"
                chunk_counts[chunk_type_str] = count + 1

                markers[name] = {
                    "offset": offset,
                    "size": full_chunk_size,
                    "type": chunk_type_str,
                    "crc_valid": stored_crc_int == computed_crc,
                }

                offset += full_chunk_size
            except Exception as e:
                print(f"[WARN] Failed to parse chunk at offset {offset}: {e}")
                break

        return markers

    def _read_metadata_chunks(self) -> dict:
        offset = 8  # PNG signature
        parsed = {}

        while offset < len(self.binary_repr):
            try:
                length = int.from_bytes(self.binary_repr[offset : offset + 4], "big")
                chunk_type = self.binary_repr[offset + 4 : offset + 8]
                chunk_data = self.binary_repr[offset + 8 : offset + 8 + length]
                offset += 12 + length  # length(4) + type(4) + data + CRC(4)

                if chunk_type == b"IHDR":
                    parsed["IHDR"] = self._parse_IHDR(chunk_data)
                elif chunk_type == b"tIME":
                    parsed["tIME"] = self._parse_tIME(chunk_data)
                elif chunk_type in [b"tEXt", b"iTXt", b"zTXt"]:
                    key = chunk_type.decode()
                    parsed.setdefault(key, []).append(
                        self._parse_text_chunk(chunk_data)
                    )
                elif chunk_type == b"pHYs":
                    parsed["pHYs"] = self._parse_pHYs(chunk_data)
                elif chunk_type == b"iCCP":
                    parsed["iCCP"] = self._parse_iCCP(chunk_data)
                elif chunk_type == PNG_CHUNK_MARKERS["eXIf"]:
                    # Parse raw EXIF bytes
                    from imagehat.identifiers.exif_attribute_information import (
                        exif_attribute_information,
                    )  # or your correct import

                    parsed["eXIf_raw"] = chunk_data.hex()
                    parsed["eXIf"] = self.parse_png_exif_chunk(
                        chunk_data, exif_attribute_information
                    )

            except Exception as e:
                print(f"[WARN] Failed to read metadata chunk at offset {offset}: {e}")
                break
        return parsed

    def parse_png_exif_chunk(
        exif_bytes: bytes, exif_attribute_information: dict
    ) -> dict:
        """
        Parses the eXIf chunk in PNG, using TIFF header logic and known EXIF tag definitions.
        Returns a dictionary of tag_name: parsed_value.
        """
        if len(exif_bytes) < 8:
            return {"Error": "EXIF chunk too short to contain a valid TIFF header."}

        byte_order = exif_bytes[0:2]
        if byte_order == b"II":
            endianness = "<"
        elif byte_order == b"MM":
            endianness = ">"
        else:
            return {"Error": f"Invalid byte order: {byte_order}"}

        # TIFF header validation (usually 0x002A)
        tag_marker = struct.unpack(f"{endianness}H", exif_bytes[2:4])[0]
        if tag_marker != 0x2A:
            return {"Error": f"Invalid TIFF tag marker: {tag_marker}"}

        # Offset to first IFD (from start of TIFF)
        first_ifd_offset = struct.unpack(f"{endianness}I", exif_bytes[4:8])[0]

        # Read number of IFD entries
        num_entries = struct.unpack(
            f"{endianness}H", exif_bytes[first_ifd_offset : first_ifd_offset + 2]
        )[0]
        tags = {}

        for entry in range(num_entries):
            entry_offset = first_ifd_offset + 2 + entry * 12
            try:
                tag, datatype, count, value = struct.unpack(
                    f"{endianness}HHII", exif_bytes[entry_offset : entry_offset + 12]
                )
            except Exception:
                continue

            tag_bytes = tag.to_bytes(2, byteorder="big")
            tag_info = exif_attribute_information.get(tag_bytes)

            if not tag_info:
                tag_name = f"Unknown_{tag_bytes.hex()}"
            else:
                tag_name = tag_info.get("name", f"Tag_{tag_bytes.hex()}")

            if datatype == 2:  # ASCII
                if count <= 4:
                    data = (
                        value.to_bytes(4, byteorder=endianness.strip("<>"))
                        .rstrip(b"\x00")
                        .decode(errors="ignore")
                    )
                else:
                    actual_offset = value
                    data = (
                        exif_bytes[actual_offset : actual_offset + count]
                        .rstrip(b"\x00")
                        .decode(errors="ignore")
                    )
            elif datatype in [3, 4]:  # SHORT or LONG
                data = value
            else:
                data = f"[Unhandled datatype: {datatype}]"

            tags[tag_name] = {"value": data, "type": datatype, "count": count}

        return tags

    def parse_tag_from_buffer(
        tag: bytes,
        data_type: int,
        count: int,
        value: int,
        entry_offset: int,
        tiff_offset: int,
        endianness: str,
        order: int,
        exif_bytes: bytes,
        tag_info: dict,
        parse_rational_fn=None,
    ) -> dict:
        """
        Generic EXIF tag parser for JPEG/PNG.
        Inputs are raw tag fields, TIFF-relative offsets, and the EXIF byte buffer.
        """
        type_name = TAG_TYPES.get(data_type, 7)
        doc_type = tag_info.get("type", None)
        doc_count = tag_info.get("count", None)

        size_of_type = TAG_TYPES.get(data_type, 1)
        total_data_length = count * size_of_type
        absolute_offset = value + tiff_offset

        is_overflow = total_data_length > 4 or type_name in OVERFLOW_TYPES
        is_big = int(value) > 1024

        if is_overflow:
            try:
                content_bytes = exif_bytes[
                    value + tiff_offset : value + tiff_offset + total_data_length
                ]
                content_offset = value

                if type_name in OVERFLOW_TYPES and parse_rational_fn:
                    content_bytes = exif_bytes[
                        value + tiff_offset : value + tiff_offset + 8
                    ]
                    value = parse_rational_fn(content_bytes, endianness)

                if is_big:
                    content_bytes = f"Deferred @ {absolute_offset} (abs offset)"

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
                    "Content Bytes": repr(content_offset),
                    "Content Value": value,
                    "IFD Tag Order": order,
                }
            except Exception as e:
                return {"Error": f"Failed to extract overflow value: {e}"}

        # Inline value (<=4 bytes)
        try:
            inline_bytes = value.to_bytes(
                4, byteorder="little" if endianness == "<" else "big"
            )
        except Exception:
            inline_bytes = b"?"

        return {
            "Markup": f"[{entry_offset}:{entry_offset+12}]",
            "Absolute Offset": entry_offset,
            "TIFF Offset": entry_offset - tiff_offset,
            "Recorded Type": data_type,
            "Type": type_name,
            "Expected Type": doc_type,
            "Count": count,
            "Expected Count": doc_count,
            "Content Bytes": inline_bytes,
            "Content Value": value,
            "IFD Tag Order": order,
        }

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
        parsed = self._read_metadata_chunks()
        exif_data = parsed.get("eXIf")

        return {
            "File Name": self.img_path,
            "EXIF Info": (
                exif_data
                if exif_data
                else {"Error": "No EXIF segment found in this PNG file."}
            ),
        }

    def get_complete_image_data(self) -> dict:
        parsed_metadata = self._read_metadata_chunks()
        exif_data = parsed_metadata.get("eXIf", None)

        return {
            "General File Info": {
                "File Name": os.path.basename(self.img_path),
                "Format": "PNG",
                "Size (bytes)": len(self.binary_repr),
            },
            "PNG Chunk Map": self._read_png_chunks(),
            "PNG Parsed Metadata": parsed_metadata,
            "EXIF Info": (
                exif_data
                if exif_data
                else {"Error": "No EXIF segment found in this PNG file."}
            ),
        }

    @classmethod
    def get_image_datas(
        cls, images: str | list, verbose: str = "complete", limit=None, segment=None
    ) -> list[dict]:
        pass


if __name__ == "__main__":
    path = r"datasets\scraped_news_images\downloaded_images\Document\fountain-pen.png"
    # path = r"C:\Users\saete\Downloads\PNG_transparency_demonstration_1.png"

    img = PNGParser(path)
    print(img.get_complete_image_data())
    print(img.binary_repr[:100])
