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
    # import traceback

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

        for root, _, files in os.walk(device_folder_path):
            for file_name in files:
                img_path = os.path.join(root, file_name)

                if img_path.lower().endswith((".jpg", ".jpeg")):
                    try:
                        parser = JPEGParser(img_path)
                        if verbose == "complete":
                            meta = parser.get_complete_image_data()
                        elif verbose == "exif":
                            meta = parser.get_exif_image_data()

                        # Fix the key: save relative path from device_folder_path
                        relative_path = os.path.relpath(img_path, base_folder)
                        all_metadata[relative_path] = meta

                    except Exception as e:
                        print(f"[ERROR] Failed to process {img_path}: {e}")
                        # traceback.print_exc()

        print(f"[INFO] Finished processing ... {device_name}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file_path = os.path.join(output_folder, f"{fname}_metadata.json")

    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(convert_bytes(all_metadata), f, indent=4)

    print(f"\n✅ Metadata saved ➔ {output_file_path}")


if __name__ == "__main__":
    start = time.time()
    # divnoise_canon1 = [
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_0\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_0\Images\Natural",
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_1\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_1\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_2\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_2\Images\Natural",
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_3\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon1\Canon_EOS6DMarkII_Rear_3\Images\Natural",
    # ]

    # divnoise_canon2 = [
    #     r"datasets\divnoise_dataset\Canon2\Canon_EOS6DMarkII_Rear_5\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon2\Canon_EOS6DMarkII_Rear_5\Images\Natural",
    #     r"datasets\divnoise_dataset\Canon2\Canon_EOS6DMarkII_Rear_6\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon2\Canon_EOS6DMarkII_Rear_6\Images\Natural",
    #     r"datasets\divnoise_dataset\Canon2\Canon_EOS6DMarkII_Rear_4\Images\Flat",
    #     r"datasets\divnoise_dataset\Canon2\Canon_EOS6DMarkII_Rear_4\Images\Natural",
    # ]

    # divnoise_canon3 = [
    #     r"D:\image_dataset\Canon3\Canon_EOS6D_Rear_0\Images\Flat",
    #     r"D:\image_dataset\Canon3\Canon_EOS6D_Rear_0\Images\Natural",
    #     r"D:\image_dataset\Canon3\Canon_EOS6D_Rear_1\Images\Flat",
    #     r"D:\image_dataset\Canon3\Canon_EOS6D_Rear_1\Images\Natural",
    #     r"D:\image_dataset\Canon3\Canon_EOS6D_Rear_2\Images\Flat",
    #     r"D:\image_dataset\Canon3\Canon_EOS6D_Rear_2\Images\Natural",
    # ]

    # divnoise_canon4 = [
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_0\Images\Flat",
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_0\Images\Natural",
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_1\Images\Flat",
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_1\Images\Natural",
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_2\Images\Flat",
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_2\Images\Natural",
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_3\Images\Flat",
    #     r"D:\image_dataset\Canon4\Canon_EOSR_Rear_3\Images\Natural",
    # ]

    # divnoise_canon5 = [
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_4\Images\Flat",
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_4\Images\Natural",
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_5\Images\Flat",
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_5\Images\Natural",
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_6\Images\Flat",
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_6\Images\Natural",
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_7\Images\Flat",
    #     r"D:\image_dataset\Canon5\Canon_EOSR_Rear_7\Images\Natural",
    # ]

    # base_name = os.path.join("D:\\", "image_dataset", "Others", "Others")

    # path_others = [
    #     os.path.join(base_name, path)
    #     for path in os.listdir(base_name)
    #     if os.path.isdir(os.path.join(base_name, path))
    # ]

    # add1 = os.path.join("Images", "Flat")
    # add2 = os.path.join("Images", "Natural")
    # divnoise_others = []
    # for path in path_others:
    #     divnoise_others.extend([os.path.join(path, add1), os.path.join(path, add2)])

    base_folder = os.path.join("datasets", "scraped_news_images")
    output_folder = os.path.join("datasets", "json_datasets", "scraped_news_images")
    process_folders(base_folder, output_folder, "scraped_news.json", verbose="complete")



    # for base_folder in divnoise_others:
    #     output_folder = os.path.join("D:", "image_dataset", "Others")
    #     name = base_folder.split("\\")[3]
    #     process_folders(base_folder, output_folder, name, verbose="complete")

    end = time.time()
    print(f"\n✅ Done in {end - start:.2f} seconds.")
