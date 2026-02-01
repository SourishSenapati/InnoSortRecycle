"""
Dataset Bootstrapper for RADORDENA.
Since real industrial battery datasets (NMC vs LFP) are often proprietary or behind
logins (Kaggle/Roboflow), this script generates a SYNTHETIC 'Placeholder' Dataset
to allow you to immediate test the training pipeline.

It also provides the LINKS to the real datasets for you to download manually.
"""

# pylint: disable=no-member
from pathlib import Path
import cv2
import numpy as np

# Config
DATASET_ROOT = Path("datasets/batteries")
CLASSES = ['NMC', 'LFP', 'Contaminant']
SPLITS = ['train', 'val']

# Real Dataset Links (for user to download later)
REAL_DATA_LINKS = {
    "Waste Classification (Kaggle)":
        "https://www.kaggle.com/datasets/techsash/waste-classification-data",
    "Battery Defect Dataset (Roboflow)":
        "https://universe.roboflow.com/search?q=battery",
    "TrashNet (GitHub)":
        "https://github.com/garythung/trashnet"
}


def create_structure():
    """
    Creates the directory structure for the dataset.
    """
    for split in SPLITS:
        for folder in ['images', 'labels']:
            path = DATASET_ROOT / split / folder
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {path}")


def generate_synthetic_sample(cls_name, img_id, split):
    """
    Generates a synthetic image and label for testing the YOLO pipeline.
    """
    # 1. Create Image (640x640)
    img = np.zeros((640, 640, 3), dtype=np.uint8)

    # Color coding
    if cls_name == 'NMC':
        color = (200, 100, 0)  # Blue-ish
        text = "NMC BATTERY"
    elif cls_name == 'LFP':
        color = (0, 200, 100)  # Green-ish
        text = "LFP BATTERY"
    else:
        color = (0, 0, 200)    # Red-ish
        text = "CONTAMINANT"

    # Draw "Battery" shape
    cv2.rectangle(img, (100, 200), (540, 440), color, -1)  # type: ignore
    cv2.putText(img, text, (150, 320), cv2.FONT_HERSHEY_SIMPLEX,  # type: ignore
                1.5, (255, 255, 255), 3)

    # Add noise to simulate real world
    noise = np.random.randint(0, 50, (640, 640, 3), dtype=np.uint8)
    img = cv2.add(img, noise)  # type: ignore

    # Save Image
    params = DATASET_ROOT / split / 'images' / f"{cls_name}_{img_id}.jpg"
    cv2.imwrite(str(params), img)  # type: ignore

    # 2. Create Label (YOLO format: class x_center y_center width height)
    # Normalized coords (0-1)
    cls_idx = CLASSES.index(cls_name)
    # Box around the rectangle we drew
    label_content = f"{cls_idx} 0.5 0.5 0.6875 0.375"

    label_path = DATASET_ROOT / split / 'labels' / f"{cls_name}_{img_id}.txt"
    with open(label_path, "w", encoding='utf-8') as f:
        f.write(label_content)


def main():
    """
    Main function to drive the dataset generation.
    """
    print("--- RADORDENA DATASET BOOTSTRAPPER ---")
    create_structure()

    print("\nGenerating Synthetic 'Placeholder' Data for Testing...")
    # Generate 50 training images and 10 validation images per class
    counts = {'train': 50, 'val': 10}

    for split, count in counts.items():
        for cls in CLASSES:
            for i in range(count):
                generate_synthetic_sample(cls, i, split)

    print(f"\nSuccess! Generated {3*60} synthetic images.")
    print("You can now run 'py train_vision_agent.py' to verify the pipeline works.")

    print("\n--- REAL DATA SOURCES ---")
    print("To train a REAL model, please manually download datasets from:")
    for name, link in REAL_DATA_LINKS.items():
        print(f"- {name}: {link}")
    print("Unzip them into the 'datasets/batteries' folder structure.")


if __name__ == "__main__":
    main()
