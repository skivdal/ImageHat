# This maps supported file extensions to the parser that handles them

from imagehat.parsers.jpeg_parser import JPEGParser

# from imagehat.parsers.mp4_parser import MP4Parser

VALID_FORMATS = {
    # JPEG family
    ".jpeg": JPEGParser,
    ".jpg": JPEGParser,
    ".jpe": JPEGParser,
    ".jfif": JPEGParser,
    ".jfi": JPEGParser,
    # # MP4 family
    # ".mp4": MP4Parser,
    # ".mov": MP4Parser
}
