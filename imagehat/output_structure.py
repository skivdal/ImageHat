# Layout of structure

EXIF_DATA_OUTPUT_STRUCTURE = {
    "name":None, # name of metadata / marker segment
    "markups":None, # beginning and end of marker
    "type":None, # data type of the metadata
    "location":None, # location / offset of metadata content
    "content":None, # byte size of content
    "status":None, # advanced feature, to be further discussed
}

_EXIF_DATA_OUTPUT_4B = {
    "Markup": f"[{entry_offset}:{entry_offset+12}]",
    "Absolute Offset": entry_offset,
    "TIFF offset": entry_offset-tiff_offset,
    "Type": data_type,
    "Doc. Type": data_type_doc,
    "Count": count,
    "Content": hex(value),
    "Content Value": value,
    "Status":None,
                    }


_EXIF_DATA_OUTPUT_L4B = {
    "Markup": f"[{entry_offset}:{entry_offset+12}]",
    "Absolute Offset":entry_offset,
    "TIFF offset":entry_offset-tiff_offset,
    "Type": data_type,
    "Doc. Type": data_type_doc,
    "Count": count,
    "Content Offset": value,
    "Content Location": tiff_offset+value,
    "Content": hex(content),
    "Content Value": content,
    "Status":None,
                }