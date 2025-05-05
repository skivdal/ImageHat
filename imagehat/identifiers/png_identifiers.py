# imagehat/identifiers/png_identifiers.py

PNG_CHUNK_MARKERS = {
    "eXIf": b"eXIf",
    "IHDR": b"IHDR",
    "iTXt": b"iTXt",
    "tEXt": b"tEXt",
    "zTXt": b"zTXt"
}

IDENTIFIERS = {
    "png_signature": b"\x89PNG\r\n\x1a\n", 
}
