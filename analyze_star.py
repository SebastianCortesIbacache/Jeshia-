"""
Script auxiliar: Analizar la posición y color de la estrella watermark
en la esquina inferior derecha de las imágenes montaje.
"""
from PIL import Image
import numpy as np

img_path = r"E:\Logo Jeshia\assets\montajes\oficiales\Mikado.png"
img = Image.open(img_path).convert("RGB")
arr = np.array(img)

h, w = arr.shape[:2]
print(f"Imagen: {w} x {h} px")

# Recorte de la esquina inferior derecha: último 15% de ancho y alto
cx = int(w * 0.85)
cy = int(h * 0.78)

crop = arr[cy:, cx:]
print(f"\nZona analizada desde ({cx},{cy}) hasta ({w},{h})")
print(f"Tamaño zona: {crop.shape[1]} x {crop.shape[0]}")

# Buscar píxeles muy blancos/brillantes (estrella blanca)
bright_mask = (crop[:,:,0] > 230) & (crop[:,:,1] > 230) & (crop[:,:,2] > 230)
ys, xs = np.where(bright_mask)
if len(xs) > 0:
    print(f"\nPíxeles brillantes encontrados: {len(xs)}")
    print(f"  X range en la zona: {xs.min()} - {xs.max()}  (global: {xs.min()+cx} - {xs.max()+cx})")
    print(f"  Y range en la zona: {ys.min()} - {ys.max()}  (global: {ys.min()+cy} - {ys.max()+cy})")
    # Muestra valores del centro de la estrella
    cx_star = int((xs.min() + xs.max()) / 2) + cx
    cy_star = int((ys.min() + ys.max()) / 2) + cy
    print(f"\n  Centro estimado estrella: ({cx_star}, {cy_star})")
    print(f"  Color centro: {arr[cy_star, cx_star]}")
else:
    print("No se encontraron píxeles brillantes en la zona.")

# Muestra colores de la zona circundante (fondo)
sample_region = arr[cy:cy+100, cx:cx+100]
print(f"\nColor promedio del fondo en zona ({cx},{cy})+(100x100): {sample_region.mean(axis=(0,1)).astype(int)}")
