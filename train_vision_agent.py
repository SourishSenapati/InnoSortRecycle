"""
Script to train the RADORDENA-SORT-01 vision model using YOLOv8.
"""
from ultralytics import YOLO


def train_sorting_agent():
    """
    Train the YOLOv8 nano model on the battery dataset for classification.
    """
    # Load a pre-trained model (transfer learning)
    # 'yolov8n.pt' is the nano version, perfect for RTX 4050
    model = YOLO('yolov8n.pt')

    # Train the model
    model.train(
        data='batteries_config.yaml',  # Points to your dataset
        epochs=50,                    # 50 loops through data
        imgsz=640,                    # Image resolution
        device=0,                     # Use the RTX 4050 (GPU 0)
        batch=16,                     # Batch size that fits in 6GB VRAM
        name='radordena_sort_v1'
    )

    # Export for deployment
    model.export(format='onnx')  # Fast format for production


if __name__ == '__main__':
    try:
        train_sorting_agent()
    except KeyboardInterrupt:
        print("\nTraining interrupted. YOLOv8 automatically saves checkpoints during training.")
        print("Check the 'runs/' directory for 'last.pt'.")
