# Layout of output structure

# Used if count or recorded type surpasses 4 bytes
OVERFLOW_OUTPUT_STRUCTURE = {
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

BASIC_OUTPUT_STRUCTURE = { 
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