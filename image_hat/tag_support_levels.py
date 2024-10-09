

# Types related to tags according to the EXIF standard
# These types represents bytes

BYTE = 1 # An 8-bit unsigned integer.
ASCII = 2 # An 8-bit byte containing one 7-bit ASCII code. Final bute is terminated with NULL. 1 per character.
SHORT = 3 # A 16-bit unsigned integer.
LONG = 4 # A 32-but usinged intege.
RATIONAL = 5 # Two LONGs, first LONG is the numerator and the second LONG expresses the denominator.
SIGNED_BYTE = 6 # RARE IN TIFF. A 8-bit signed integer.
UNDEFINED = 7  # An 8-bit byte that may take any value depending on the field defenition. Often used for unstructured binary data. 
SINGED_SHORT = 8 # A 16-bit signed integer. 
SIGNED_LONG = 9 # A 32-bit signed integer. 
SIGNED_RATIONAL = 10 # Two SIGNED_LONGs values. 64-bits in total (32 + 32).
FLOAT = 11 # A 32-bit single-precision floating-point number. 
DOUBLE = 12 # A 64-bit double-precision floating-point number.
UTF_8 = 129 # An 8-bit integer representing a string according to UTF-8


# Recording Notation Level
Notation = {
    "M":"Mandatory",
    "R":"Recommended",
    "O":"Optional",
    "N":"It is not allowed to record"     
}


# Table 14 in JEITA docs. GPS Atrrib. Information

EXIF_SPECIFIC_TAGS = {
    
}

TIFF_SPECIFIC_TAGS = {

}