import os
import json
import time
from imagehat.parsers.jpeg_parser import JPEGParser


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


def process_folders(
    base_folder: str, output_folder: str, fname: str, verbose: str = "complete"
):

    if not os.path.isdir(base_folder):
        print(f"[ERROR] Base folder does not exist: {base_folder}")
        return ValueError("Could not see: {basefolder} due to {error}")

    print(f"[INFO] Searching and processing Dresden images in {base_folder}...\n")

    all_metadata = {}

    for device_name in os.listdir(base_folder):
        device_folder_path = os.path.join(base_folder, device_name)

        if not os.path.isdir(device_folder_path):
            continue  # Skip if not a folder

        print(f"[INFO] Processing folder ... {device_name}")

        for file_name in os.listdir(device_folder_path):
            img_path = os.path.join(device_folder_path, file_name)

            if img_path.lower().endswith((".jpg", ".jpeg")):
                try:
                    parser = JPEGParser(img_path)
                    if verbose == "complete":
                        meta = parser.get_complete_image_data()
                    elif verbose == "exif":
                        meta = parser.get_exif_image_data()

                    metrics = parser.compute_conformity_metrics()
                    meta["Metrics"] = metrics

                    full_key = os.path.join(device_name, file_name)
                    all_metadata[full_key] = meta

                except Exception as e:
                    print(f"[ERROR] Failed to process {img_path}: {e}")
        print(f"[INFO] Finished processing ... {device_name}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file_path = os.path.join(output_folder, f"{fname}_metadata.json")

    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(convert_bytes(all_metadata), f, indent=4)

    print(f"\n✅ Metadata saved ➔ {output_file_path}")


if __name__ == "__main__":
    start = time.time()

    # base_folder = os.path.join("datasets", "divnoise_dataset", "Canon1")
    # output_folder = os.path.join("json_datasets", "divnoise_images")

    # base_folder = os.path.join("datasets", "divnoise_dataset", "Canon2")
    # output_folder = os.path.join("json_datasets", "divnoise_images")

    base_folder = os.path.join("datasets", "archive", "Dresden_Exp")
    output_folder = os.path.join("datasets", "json_datasets", "dresden_images")

    process_folders(base_folder, output_folder, "dresden", verbose="complete")

    # end = time.time()
    # print(f"\n✅ Done in {end - start:.2f} seconds.")

    ##can you tweek this file such that i can search through in the folder branches of divnoise dataset and return json files as found in json_datasets/dresden_images
    ##and also add a function to save the json files in the same folder as the images

    # NOTE that this function is used for divnoise dataset structure only
    # def get_all_jpg_folders(base_folder: str) -> list:
    #     """
    #     Recursively searches for folders named 'JPG' in the directory tree starting from base_folder.

    #     :param base_folder: Root directory to start the search.
    #     :type base_folder: str

    #     :return: List of relative paths to folders named 'JPG'.
    #     :rtype: list
    #     """
    #     jpg_folders = []
    #     for root, dirs, files in os.walk(base_folder):
    #         for dir_name in dirs:
    #             if dir_name == "JPG":
    #                 relative_path = os.path.relpath(os.path.join(root, dir_name), base_folder)
    #                 jpg_folders.append(relative_path)
    #     return jpg_folders

    # jpg_folders_list = get_all_jpg_folders("datasets/divnoise_dataset/Others")
    # print(jpg_folders_list)

    # divnoise_part0 = [
    #     "Canon1/Canon_EOS6DMarkII_Rear_0/Images/Flat/JPG",
    #     "Canon1/Canon_EOS6DMarkII_Rear_0/Images/Natural/JPG",
    #     "Canon1/Canon_EOS6DMarkII_Rear_1/Images/Flat/JPG",
    #     "Canon1/Canon_EOS6DMarkII_Rear_1/Images/Natural/JPG",
    #     "Canon1/Canon_EOS6DMarkII_Rear_2/Images/Flat/JPG",
    #     "Canon1/Canon_EOS6DMarkII_Rear_2/Images/Natural/JPG",
    #     "Canon1/Canon_EOS6DMarkII_Rear_3/Images/Flat/JPG",
    #     "Canon1/Canon_EOS6DMarkII_Rear_3/Images/Natural/JPG",
    # ]
