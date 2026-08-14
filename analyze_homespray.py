"""
Analiza la estrella en Home Spray.png con mas detalle
"""
from PIL import Image
import numpy as np

img_path = "E:/Logo Jeshia/assets/montajes/oficiales/Home Spray.png"
img = Image.open(img_path).convert("RGB")
arr = np.array(img)
h, w = arr.shape[:2]
print(f"Imagen: {w} x {h} px")

# Zona inferior derecha
cx = int(w * 0.85)
cy = int(h * 0.78)
crop = arr[cy:, cx:]
print(f"Zona desde ({cx},{cy})")

# Color fondo estimado
bg = arr[cy:cy+80, cx:cx+80].mean(axis=(0,1))
print(f"Color fondo: {bg.astype(int)}")

# Buscar pixeles MAS brillantes que el fondo (>10 pts)
for threshold in [10, 15, 18, 20, 25]:
    diff = crop.astype(float).mean(axis=2) - bg.mean()
    bright_mask = diff > threshold
    ys, xs = np.where(bright_mask)
    print(f"  Threshold {threshold}: {len(xs)} pixeles")
    if len(xs) > 0 and threshold == 10:
        print(f"    X: {xs.min()+cx} - {xs.max()+cx}, Y: {ys.min()+cy} - {ys.max()+cy}")
        print(f"    Color max: {crop[ys, xs].max(axis=0)}")
        print(f"    Color mean: {crop[ys, xs].mean(axis=0).astype(int)}")
