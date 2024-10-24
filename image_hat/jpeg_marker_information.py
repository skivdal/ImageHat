# Information of all the applied markers segments found in .JPEG


MARKER_SEGMENTS_JPEG = {
    b"\xFF\xD8": "SOI (Start of Image)",
    b"\xFF\xE1": "APP1 (EXIF Application Marker)",
    b"\xFF\xDB": "DQT (Define Quantization Table)",
    b"\xFF\xC4": "DHT (Define Huffman Table)",
    b"\xFF\xDD": "(DRI (Restart Interval))",
    b"\xFF\xC0": "SOF0 (Start of Frame | Baseline DCT)",    
    b"\xFF\xC1": "SOF1 (Start of Frame | Extended Sequential DCT)",
    b"\xFF\xC2": "SOF2 (Start of Frame | Progressive DCT)",    
    b"\xFF\xC3": "SOF3 (Start of Frame | Lossless JPEG)",    
    b"\xFF\xDA": "SOS (Scan Header)",
    b"\xFF\xD9": "EOI (End of Image)"
}

#MARKER_SEGMENTS_JPEG_REV = {(v,k) for k,v in MARKER_SEGMENTS_JPEG.items()}

