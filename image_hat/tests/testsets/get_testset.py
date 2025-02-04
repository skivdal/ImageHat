import os
import random
import shutil

# Define the path to the test set folder
base_folder = r"dataset\archive\Dresden_Exp"

# Define the destination folder for the selected images
output_folder = "./image_hat/tests/testsets/testset-small"
os.makedirs(output_folder, exist_ok=True)

# Loop through each camera model folder
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)

    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Get all image files in the folder
        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Select 10 random images or all if less than 10
        selected_files = random.sample(image_files, min(len(image_files), 1))

        # Copy selected images to the output folder
        for file_name in selected_files:
            src_file = os.path.join(folder_path, file_name)
            dst_file = os.path.join(output_folder, f"{folder_name}_{file_name}")  # Prefix file names with folder name
            shutil.copy(src_file, dst_file)

print(f"Random images have been selected and saved to '{output_folder}'")
