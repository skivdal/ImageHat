import os
import json
import time
from imagehat.parsers import JPEGParser


def collect_image_paths(base_path, extensions=(".jpg", ".jpeg", ".webp")):
    image_paths = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(extensions):
                full_path = os.path.join(root, file)
                image_paths.append(full_path)
    return image_paths


start_time = time.time()

# base_dir = r"D:\image_dataset\Images\Dresden_image_dataset"
# base_dir = r"D:\image_dataset\Images\Divnoise_image_dataset"
base_dir = r"datasets\scraped_news_images\downloaded_images"

image_paths = collect_image_paths(base_dir)


dataset = {}
for path in image_paths:
    try:
        data = JPEGParser(path).get_complete_image_data()
        dataset[path] = data
    except Exception as e:
        print(f"Failed to parse {path}: {e}")


with open("scraped_news_metadata.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2)

end_time = time.time()
elapsed = end_time - start_time
print(f"\n✅ Done! Processed {len(dataset)} files in {elapsed:.2f} seconds.")
