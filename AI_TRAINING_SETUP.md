# RADORDENA AI Training Setup (RTX 4050 Optimized)

## Strategic Overview

We are utilizing **Efficient Fine-Tuning (LoRA)** and **Quantized Inference (4-bit)** to train and run cognitive agents on the **NVIDIA RTX 4050 (6GB VRAM)**.

## 0. Environment Setup

### System Prerequisites

1. **NVIDIA Drivers:** Ensure latest drivers are installed.
2. **CUDA Toolkit:** Version 11.8 or 12.1.

### Python Environment (Conda Recommended)

```bash
conda create -n radordena_ai python=3.10
conda activate radordena_ai
```

### AI Dependencies (CUDA Optimized)

```bash
# PyTorch with CUDA 11.8 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Cognitive Agent Libraries
# ultralytics: For YOLOv8/ViT Vision Agent
# stable-baselines3: For DRL Core Agent
pip install ultralytics stable-baselines3 shimmy
```

## 1. Verification

Run the following python script to verify CUDA availability:

```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"Device Name: {torch.cuda.get_device_name(0)}")
```
