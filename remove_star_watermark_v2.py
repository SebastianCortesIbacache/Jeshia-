# -*- coding: utf-8 -*-
"""
remove_star_watermark_v2.py
Elimina la estrella blanca de 4 puntas (watermark) esquina inferior derecha.
Guarda como '[nombre] without watermark.png'

Enfoque: busqueda adaptativa de la estrella en zona inferior derecha,
con umbral dinamico segun el brillo del fondo local.
"""
from PIL import Image
import numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter

OFICIALES_DIR = Path("E:/Logo Jeshia/assets/montajes/oficiales")

# La estrella siempre esta en el cuadrante inferior derecho.
# Buscaremos dentro del 20% final en X y el 30% final en Y.
SEARCH_X_START = 0.72
SEARCH_Y_START = 0.72


def find_star_bbox(arr, search_x=SEARCH_X_START, search_y=SEARCH_Y_START):
    """
    Localiza la estrella blanca en la zona inferior derecha.
    Retorna (x1, y1, x2, y2) del bounding box, o None si no la encuentra.
    """
    h, w = arr.shape[:2]
    sx = int(w * search_x)
    sy = int(h * search_y)
    
    zone = arr[sy:, sx:].astype(float)
    
    # Medir color promedio del fondo local (usamos percentil 25 para evitar la estrella)
    bg_channel_means = []
    for c in range(3):
        ch = zone[:, :, c].flatten()
        bg_channel_means.append(np.percentile(ch, 25))
    bg_mean = np.mean(bg_channel_means)
    
    # Luminosidad de cada pixel en la zona
    zone_lum = zone.mean(axis=2)
    
    # Umbral adaptativo: pixels que destacan al menos 8 pts sobre el fondo
    threshold = 8
    bright_mask = zone_lum > (bg_mean + threshold)
    
    ys, xs = np.where(bright_mask)
    if len(xs) < 10:
        return None
    
    # Filtrar outliers (tomamos el 95% central del cluster)
    x_p5, x_p95 = np.percentile(xs, [2, 98])
    y_p5, y_p95 = np.percentile(ys, [2, 98])
    
    margin = 30  # margen adicional en pixels
    x1 = max(0, int(x_p5) + sx - margin)
    y1 = max(0, int(y_p5) + sy - margin)
    x2 = min(w, int(x_p95) + sx + margin)
    y2 = min(h, int(y_p95) + sy + margin)
    
    return x1, y1, x2, y2


def sample_border_colors(arr, x1, y1, x2, y2, border=50):
    """
    Muestrea colores del fondo alrededor del bounding box.
    Retorna colores medios para los 4 bordes (top, bottom, left, right).
    """
    h, w = arr.shape[:2]
    
    def sample(row_s, col_s):
        region = arr[row_s, col_s].astype(float)
        if region.size == 0:
            return np.array([230.0, 220.0, 210.0])
        flat = region.reshape(-1, 3)
        # Excluir pixeles extremadamente brillantes
        lum = flat.mean(axis=1)
        valid = flat[lum < 252]
        return valid.mean(axis=0) if len(valid) > 5 else flat.mean(axis=0)
    
    top    = sample(slice(max(0, y1-border), max(0, y1)), slice(x1, x2))
    bottom = sample(slice(min(h, y2), min(h, y2+border)), slice(x1, x2))
    left   = sample(slice(y1, y2), slice(max(0, x1-border), max(0, x1)))
    right  = sample(slice(y1, y2), slice(min(w, x2), min(w, x2+border)))
    
    return top, bottom, left, right


def make_gradient_patch(x1, y1, x2, y2, top, bottom, left, right):
    """
    Genera patch con gradiente bilineal usando los 4 colores de borde.
    Vectorizado (rapido sin loops).
    """
    h_p = y2 - y1
    w_p = x2 - x1
    
    # Grids de 0..1
    yy = np.linspace(0, 1, h_p)[:, np.newaxis]   # (h_p, 1)
    xx = np.linspace(0, 1, w_p)[np.newaxis, :]   # (1, w_p)
    
    patch = np.zeros((h_p, w_p, 3), dtype=float)
    for c in range(3):
        # Bilinear interpolation from the 4 edges
        h_interp = left[c] * (1 - xx) + right[c] * xx   # horizontal
        v_interp = top[c]  * (1 - yy) + bottom[c] * yy  # vertical
        patch[:, :, c] = (h_interp + v_interp) / 2.0
    
    return np.clip(patch, 0, 255).astype(np.uint8)


def remove_star(img_path: Path, out_path: Path):
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8).copy()
    h, w = arr.shape[:2]
    
    print(f"\nProcesando: {img_path.name}  ({w}x{h})")
    
    bbox = find_star_bbox(arr)
    if bbox is None:
        print("  [WARN] Estrella no detectada, copiando imagen sin cambios.")
        img.save(out_path, format="PNG")
        return
    
    x1, y1, x2, y2 = bbox
    print(f"  Estrella detectada: ({x1},{y1}) -> ({x2},{y2})")
    
    # Muestrar colores de fondo circundante
    top, bottom, left, right = sample_border_colors(arr, x1, y1, x2, y2)
    
    # Crear patch gradiente
    patch = make_gradient_patch(x1, y1, x2, y2, top, bottom, left, right)
    
    # Detectar la forma exacta de la estrella (pixels mas brillantes que el fondo)
    region = arr[y1:y2, x1:x2].astype(float)
    bg_lum = np.mean([top.mean(), bottom.mean(), left.mean(), right.mean()])
    region_lum = region.mean(axis=2)
    diff = region_lum - bg_lum
    
    # Mascara con umbral bajo (8 pts) para capturar hasta los bordes suaves de la estrella
    star_mask = np.clip((diff - 6) / 12.0, 0, 1)  # 0 en pixels iguales al fondo, 1 en estrella pura
    
    # Suavizar mascara para bordes imperceptibles
    feather = gaussian_filter(star_mask, sigma=5)
    feather = np.clip(feather, 0, 1)
    
    n_affected = (feather > 0.1).sum()
    print(f"  Pixels afectados: {n_affected}")
    
    # Blend: original * (1 - mask) + patch * mask
    patch_f = patch.astype(float)
    for c in range(3):
        region[:, :, c] = region[:, :, c] * (1 - feather) + patch_f[:, :, c] * feather
    
    arr[y1:y2, x1:x2] = np.clip(region, 0, 255).astype(np.uint8)
    
    result = Image.fromarray(arr)
    result.save(out_path, format="PNG", optimize=False)
    print(f"  [OK] -> {out_path.name}")


def main():
    images = sorted([
        p for p in OFICIALES_DIR.glob("*.png")
        if "without watermark" not in p.stem.lower()
    ])
    
    print(f"Imagenes a procesar: {len(images)}")
    for img_path in images:
        stem = img_path.stem
        out_path = img_path.parent / f"{stem} without watermark.png"
        remove_star(img_path, out_path)
    
    print("\n[DONE] Proceso completado.")


if __name__ == "__main__":
    main()
