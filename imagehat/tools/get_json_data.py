import os
import json
from imagehat.parsers.jpeg_parser import JPEGParser
from imagehat.tools.formats import VALID_FORMATS


def convert_bytes(obj):
    """
    Recursively convert bytes to hex for JSON compatibility.

    :param obj: The object to convert.
    :type obj: dict, list, bytes, or any
    :return: JSON-compatible object
    :rtype: Any
    """
    if isinstance(obj, dict):
        return {key: convert_bytes(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_bytes(value) for value in obj]
    elif isinstance(obj, bytes):
        return obj.hex()
    return obj


def extract_metadata_from_folder(folder_path: str, verbose: str = None) -> dict:
    """
    Extracts metadata from all JPEG images in a folder.

    :param folder_path: Path to the folder containing images.
    :type folder_path: str
    :param verbose: Verbosity mode. Options:
                    - None (default): Returns full metadata.
                    - "exif": Returns only EXIF metadata.
    :type verbose: str, optional

    :return: Dictionary of image filenames mapped to metadata.
    :rtype: dict
    """
    image_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(tuple(VALID_FORMATS.keys()))
    ]

    if not image_files:
        print(f"Skipping {folder_path}: No valid JPEG images found.")
        return {}

    metadata = {}
    for img in image_files:
        parser = JPEGParser(img)
        if verbose == "exif":
            data = parser.get_exif_data()
        else:
            data = parser.get_complete_image_data()
        metadata[os.path.basename(img)] = data

    return convert_bytes(metadata)


def save_metadata_to_json(
    folder_path: str,
    output_folder: str = "imagehat/datasets/json_datasets",
    verbose: str = None,
):
    """
    Extracts metadata from images in a folder and saves it as a JSON file.

    :param folder_path: Path to the folder containing images.
    :type folder_path: str
    :param output_folder: Directory where the JSON file will be saved.
    :type output_folder: str
    :param verbose: Verbosity mode. Options:
                    - None (default): Full metadata.
                    - "exif": Only EXIF metadata.
    :type verbose: str, optional

    :return: None
    """
    try:
        folder_name = os.path.basename(os.path.normpath(folder_path))
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"{folder_name}_metadata.json")

        metadata = extract_metadata_from_folder(folder_path, verbose=verbose)

        if not metadata:
            return

        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(metadata, json_file, indent=4)

        print(f"Metadata saved for folder '{folder_name}' → {output_path}")

    except Exception as e:
        print(f"Error processing folder '{folder_path}': {e}")


def process_all_subfolders(base_folder: str, verbose: str = None):
    """
    Iterates through all subfolders in a base directory and extracts metadata.

    :param base_folder: Root directory containing subfolders.
    :type base_folder: str
    :param verbose: Verbosity mode. See `save_metadata_to_json`.
    :type verbose: str, optional

    :return: None
    """
    if not os.path.isdir(base_folder):
        print(f"Error: The directory '{base_folder}' does not exist.")
        return

    print("Processing folders in:", base_folder, "...")

    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        if os.path.isdir(folder_path):
            save_metadata_to_json(folder_path, verbose=verbose)

    print("Processing complete.")


if __name__ == "__main__":
    # Example usage when run directly (not imported)
    base_folder = "datasets/archive/Dresden_Exp"
    process_all_subfolders(base_folder)
