## ImageHat Project Description

### Overview

**ImageHat** is a Python package designed to extract and inspect metadata from binary image and video files. The project focuses on providing a powerful yet user-friendly interface for analyzing EXIF metadata, identifying structural properties, and enabling deeper insights into file formats like JPEG, MP4, and more.

Whether you're working with digital images or videos, **ImageHat** equips you with the tools to parse, visualize, and manage metadata directly from binary data.
ImageHat is still in development and is limited to: **.JPEG, .JPG**

---

### Extracting EXIF Metadata from Binary Image and Video Files

EXIF (Exchangeable Image File Format) metadata provides essential information about an image or video, such as camera settings, geolocation data, timestamps, and more. **ImageHat** enables you to locate, extract, and interpret this metadata efficiently by analyzing the raw binary structure of supported file formats.

---

### Features

- **Extract EXIF Metadata**: Locate and extract metadata such as timestamps, geolocation, and device-specific information.
- **Inspect Structural Properties**: Analyze the binary structure of image and video files, including key markers like APP1 segments, SOI (Start of Image), and EOI (End of Image).
- **Support for Mainly JPEG and MP4**: Currently supports JPEG and HEIC, with plans to extend support for formats like NEF (Nikon RAW) and MP4.
- **Binary Analysis**: Identify marker positions, metadata offsets, and associated data in raw binary files.
- **Efficient Searching**: Quickly find specific tags, markers, or patterns using optimized binary search methods.
- **Customizable Metadata Extraction**: Extract and summarize specific tags or groups of tags based on your needs.

---

### Planned Features

- **Support for Additional Formats**: Expand compatibility to include formats like TIFF, MP4, and AVI.
- **Metadata Editing**: Modify EXIF metadata while preserving the structural integrity of the file.
- **Visualization Tools**: Generate visual representations of metadata relationships and tag distributions.
- **Enhanced Performance**: Optimize binary parsing for large files using parallel processing.

---

### Getting Started

#### Requirements

- Python 3.8 or later
- Required Python Libraries: all current dependecies are built-in

#### Installation

##### **- 1 Clone the Repository**

Open a terminal and run:

```sh
git clone https://github.com/YOUR_USERNAME/ImageHat.git
cd ImageHat
```

##### **- 2 Create and Activate a Virtual Environment**

- For windows (CMD, Terminal or PowerShell)

```sh
python -m venv .venv
source .venv\Scripts\activate
```

- For macOS/Linux (Terminal)

```sh
python3 -m venv .venv
source .venv/bin/activate
```

##### **- 3 Install Dependencies**

```sh
pip install -r requirements.txt
```

or if you are also using uv:

```
uv pip install -r requirements.txt
```

Sometimes you may need to create a symlink:

```sh
pip install -e .
```

#### Example Usage

```python
from imagehat import JPEGParser

# Initialize with a file path pf image or folder
file_path_image = "path/to/your/image.jpg"
testset_folder = os.path.join("tests", "testsets", "testset-small") # testset_small or testset_large is included

# Create a Parser Object and apply EXIF or complete method
img = JPEGParser(file_path_image)
print(img.get_exif_image_data())

# Apply the method on a folder 
images = JPEGParser.get_image_datas(folder_path=testset_)

# Find and summarize metadata
tags = image.extract_tags(TIFF_SPECIFIC_ATTRIBS, TYPE_SIZE_BYTES)
image.summarize_metadata(tags)
```
