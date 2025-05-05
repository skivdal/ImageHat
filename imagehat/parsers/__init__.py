# imagehat/parsers/__init__.py

import os

from imagehat.parsers.jpeg_parser import JPEGParser
from imagehat.parsers.png_parser import PNGParser
# from imagehat.parsers.webp_parser import WebPParser
# from imagehat.parsers.heic_parser import HEICParser


# Registry: maps lowercase extensions to parser classes
PARSER_REGISTRY = {
    '.jpg': JPEGParser,
    '.jpeg': JPEGParser,
    '.png': PNGParser,
    # '.webp': WebPParser,
    # '.heic': HEICParser
}


def get_parser(filepath: str):
    """
    Detects the file extension and returns the correct parser instance.
    
    :param filepath: Path to the image file.
    :return: A parser instance matching the file type.
    :raises: NotImplementedError if format is not supported.
    """
    ext = os.path.splitext(filepath)[1].lower()
    parser_cls = PARSER_REGISTRY.get(ext)

    if parser_cls is None:
        raise NotImplementedError(f"No parser available for extension: {ext}")
    
    return parser_cls(filepath)
