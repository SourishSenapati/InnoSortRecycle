"""
Data Ingestion Script for RADORDENA.
Unpacks user-provided Kaggle/Roboflow zip files and formats them for YOLOv8 training.
"""
import os
import shutil
import zipfile
from pathlib import Path
import random
import cv2
import numpy as np

# Config
DATASET_ROOT = Path("datasets/batteries")
ZIP_NAME = "archive.zip"  # We expect the user to name it this or we look for any zip
CLASSES = ['NMC', 'LFP', 'Contaminant']


def find_zip_file():
    """Finds the first zip file in the current directory."""
    cwd = Path(".")
    zips = list(cwd.glob("*.zip"))
    if not zips:
        return None
    # Prefer 'archive.zip' if it exists
    for z in zips:
        if "archive" in z.name.lower() or "achive" in z.name.lower():
            return z
    return zips[0]


def unpack_and_process(zip_path):
    print(f"📦 Found dataset: {zip_path}")
    extract_path = Path("temp_extracted_data")
    if extract_path.exists():
        shutil.rmtree(extract_path)
    extract_path.mkdir()

    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    print("Scanning for images...")
    # Find all images recursively
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    all_images = []

    for path in extract_path.rglob("*"):
        if path.suffix.lower() in image_extensions:
            all_images.append(path)

    print(f"Found {len(all_images)} images.")

    if len(all_images) == 0:
        print("❌ No images found in zip!")
        return

    print("Processing and formatting for YOLO...")

    # Counter
    processed_count = 0

    for img_path in all_images:
        # Heuristic Classification based on folder name
        parent_name = img_path.parent.name.lower()

        # Default Logic:
        # If folder has "battery" -> Randomly assign NMC(0) or LFP(1) (since we can't tell visually easily)
        # Else -> Contaminant(2)

        if "batt" in parent_name:
            # Random split 50/50 for simulation
            cls_name = random.choice(['NMC', 'LFP'])
        else:
            cls_name = 'Contaminant'

        # Determine Split (80% train, 20% val)
        split = 'train' if random.random() < 0.8 else 'val'

        # Read Image
        img = cv2.imread(str(img_path))
        if img is None:
            continue

        # Resize to 640x640 (standardize)
        img = cv2.resize(img, (640, 640))

        # Save Name
        filename = f"{cls_name}_{processed_count}_{img_path.name}"
        save_img_path = DATASET_ROOT / split / 'images' / filename
        save_img_path.parent.mkdir(
            parents=True, exist_ok=True)  # Ensure dir exists

        cv2.imwrite(str(save_img_path), img)

        # Create Dummy Label (Full Box)
        # This teaches the agent to "detect" the object filling the frame
        # Class X_center Y_center Width Height
        cls_idx = CLASSES.index(cls_name)
        label_content = f"{cls_idx} 0.5 0.5 0.99 0.99"

        save_label_path = DATASET_ROOT / split / \
            'labels' / f"{save_img_path.stem}.txt"
        save_label_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_label_path, "w", encoding='utf-8') as f:
            f.write(label_content)

        processed_count += 1

        if processed_count % 100 == 0:
            print(f"Processed {processed_count} images...", end='\r')

    print(f"\n✅ Processing Complete!")
    print(f"Imported {processed_count} images into {DATASET_ROOT}")
    print("Cleaning up temp files...")
    shutil.rmtree(extract_path)
    print("Ready for training: 'py train_vision_agent.py'")


if __name__ == "__main__":
    z_file = find_zip_file()
    if z_file:
        unpack_and_process(z_file)
    else:
        print("❌ No zip file found in current directory!")
        print("Please move your 'archive.zip' (or any .zip) into this folder:")
        print(f"   {Path('.').absolute()}")
