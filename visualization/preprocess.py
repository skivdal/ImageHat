import os
import csv
import json


def process_json_to_csv(json_path, output_csv, dataset_name):
    rows = []

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for image_name, image_info in data.items():
        try:
            exif_data = image_info.get("APP1 Info", {}).get("EXIF IFD Data", {})
            filename = image_name.split("\\")[-1]

            for tag_name, r in exif_data.items():
                rows.append(
                    {
                        "image_name": filename,
                        "tag_name": tag_name,
                        "type": r.get("Type"),
                        "doc_type": r.get("Expected Type"),
                        "tag_order": r.get("IFD Tag Order"),
                        "byte_count": r.get("Count"),
                        "source_dataset": dataset_name,
                    }
                )
        except Exception as e:
            print(f"{image_name} Error: {e}")
            continue

    if not rows:
        print(f"No EXIF metadata found in: {json_path}")
        return

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, rows[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(rows)

    print(f"Exported {len(rows)} EXIF rows to {output_csv}")
    return rows


def write_combined_csv(all_rows, output_path):
    if not all_rows:
        print("No rows to write to combined dataset.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, all_rows[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(all_rows)

    print(f"Combined dataset written to: {output_path}")


def main():
    dresden_json = (
        r"C:\Users\saete\OneDrive\Skrivebord\dresden_images\dresden_metadata_full.json"
    )
    divnoise_json = (
        r"C:\Users\saete\OneDrive\Skrivebord\divnoise_images\divnoise_dataset_full.json"
    )

    dresden_csv = "visualization/public/dresden_exif.csv"
    divnoise_csv = "visualization/public/divnoise_exif.csv"
    combined_csv = "visualization/public/updated_dataset.csv"

    # Process EXIF data only
    dresden = process_json_to_csv(dresden_json, dresden_csv, "Dresden")
    divnoise = process_json_to_csv(divnoise_json, divnoise_csv, "DivNoise")

    write_combined_csv(dresden + divnoise, combined_csv)


if __name__ == "__main__":
    main()
