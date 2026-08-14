# -*- coding: utf-8 -*-
"""
Inspect all original images in E:/Logo Jeshia/assets/montajes/oficiales
"""
from PIL import Image
from pathlib import Path

dir_path = Path("E:/Logo Jeshia/assets/montajes/oficiales")
files = sorted([f for f in dir_path.glob("*.png") if "watermark" not in f.stem.lower()])

print("ARCHIVOS ORIGINALES:")
for f in files:
    img = Image.open(f)
    print(f"  {f.name}: {img.size[0]} x {img.size[1]} px (Aspect Ratio: {img.size[0]/img.size[1]:.3f})")
