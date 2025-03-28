import os
import csv
import json


def main():
    """Read all JSON files, create CSV contaning all tags"""
    dataset_folder = "datasets/json_datasets"
    data_files = [os.path.join(dataset_folder, x) for x in os.listdir(dataset_folder)]

    rows = []
    for json_file in data_files:
        with open(json_file, 'r') as f:
            data = json.load(f)

        for image_name, image_info in data.items():
            exif_rows = image_info["APP1 Info"]["EXIF Info"]["EXIF Data"]

            for tag_name, r in exif_rows.items():
                rows.append({
                    "image_name": image_name,
                    "tag_name": tag_name,

                    "type": r["Type"],
                    "doc_type": r["Doc Type"],

                    "tag_order": r["Tag Order"],
                    "byte_count": r["Count"],
                })

    if len(rows) == 0:
        print(f"Could not find any metadata information in '{dataset_folder}'")
        return

    with open("visualization/public/dataset.csv", 'w', newline="") as f:
        dict_writer = csv.DictWriter(f, rows[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(rows)


if __name__ == "__main__":
    main()

