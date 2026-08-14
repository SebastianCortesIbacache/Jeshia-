# -*- coding: utf-8 -*-
"""
remove_star_final.py - Eliminacion quirurgica de estrellas watermark.
Usa coordenadas conocidas precisas de la estrella, detectadas manualmente
mediante analisis previo. Cubre SOLO la zona de la estrella con
inpainting por muestreo del fondo circundante.
"""
from PIL import Image
import numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter

OFICIALES_DIR = Path("E:/Logo Jeshia/assets/montajes/oficiales")

# Coordenadas de la estrella como FRACCION del tamano de la imagen.
# Calculadas del analisis: la estrella esta en la esquina inferior derecha
# y su centro esta aprox. en (91.4%, 84.3%) del tamano total.
# El radio de la estrella es aprox 4% del ancho y 6% del alto.
# Usamos un bounding box generoso de 8% x 12%.
STAR_CX_FRAC = 0.914   # Centro X
STAR_CY_FRAC = 0.843   # Centro Y  
STAR_HW_FRAC = 0.048   # Half-width
STAR_HH_FRAC = 0.070   # Half-height

# Margen de muestreo del fondo (en pixeles)
SAMPLE_BORDER = 60


def inpaint_region(arr, x1, y1, x2, y2):
    """
    Rellena la region [y1:y2, x1:x2] con interpolacion del fondo
    circundante. Solo modifica pixels que son significativamente
    mas brillantes que el fondo local.
    """
    h, w = arr.shape[:2]
    
    # === Muestrear colores de fondo en los 4 lados ===
    def get_bg(row_s, col_s, exclude_bright=True):
        region = arr[row_s, col_s].astype(float)
        if region.size == 0:
            return None
        flat = region.reshape(-1, 3)
        if exclude_bright:
            lum = flat.mean(axis=1)
            valid = flat[lum < flat.mean() + 30]
            if len(valid) > 3:
                flat = valid
        return flat.mean(axis=0)
    
    sb = SAMPLE_BORDER
    top_col    = get_bg(slice(max(0,y1-sb), y1),     slice(x1, x2))
    bot_col    = get_bg(slice(y2, min(h,y2+sb)),     slice(x1, x2))
    left_col   = get_bg(slice(y1, y2),               slice(max(0,x1-sb), x1))
    right_col  = get_bg(slice(y1, y2),               slice(x2, min(w,x2+sb)))
    
    # Fallback si alguno es None
    fallback = np.array([230.0, 215.0, 205.0])
    top_col   = top_col   if top_col   is not None else fallback
    bot_col   = bot_col   if bot_col   is not None else fallback
    left_col  = left_col  if left_col  is not None else fallback
    right_col = right_col if right_col is not None else fallback
    
    h_p = y2 - y1
    w_p = x2 - x1
    
    # === Crear patch con gradiente bilineal ===
    yy = np.linspace(0, 1, h_p)[:, np.newaxis]
    xx = np.linspace(0, 1, w_p)[np.newaxis, :]
    
    patch = np.zeros((h_p, w_p, 3), dtype=float)
    for c in range(3):
        h_blend = left_col[c] * (1 - xx) + right_col[c] * xx
        v_blend = top_col[c]  * (1 - yy) + bot_col[c]  * yy
        patch[:, :, c] = (h_blend + v_blend) / 2.0
    patch = np.clip(patch, 0, 255)
    
    # === Mascara adaptativa de la estrella ===
    region_f = arr[y1:y2, x1:x2].astype(float)
    
    # El color de fondo esperado en cada punto es el patch
    diff = region_f.mean(axis=2) - patch.mean(axis=2)
    
    # Mascara: pixels que son mas brillantes que el fondo local (estrella)
    # Umbral bajo = 5 pts sobre el fondo predicho
    star_mask = np.clip((diff - 4) / 10.0, 0, 1)
    
    # Feathering suave para bordes invisibles
    feather = gaussian_filter(star_mask, sigma=6)
    feather = np.clip(feather * 1.5, 0, 1)  # boostar un poco
    
    n = (feather > 0.05).sum()
    
    # === Blend ===
    result = region_f.copy()
    for c in range(3):
        result[:, :, c] = region_f[:, :, c] * (1 - feather) + patch[:, :, c] * feather
    
    return np.clip(result, 0, 255).astype(np.uint8), n


def process_image(img_path: Path, out_path: Path):
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8).copy()
    h, w = arr.shape[:2]
    
    print(f"\nProcesando: {img_path.name}  ({w}x{h})")
    
    # Coordenadas absolutas del bbox de la estrella
    cx = int(STAR_CX_FRAC * w)
    cy = int(STAR_CY_FRAC * h)
    hw = int(STAR_HW_FRAC * w)
    hh = int(STAR_HH_FRAC * h)
    
    x1 = max(0, cx - hw)
    y1 = max(0, cy - hh)
    x2 = min(w, cx + hw)
    y2 = min(h, cy + hh)
    
    print(f"  BB estrella: ({x1},{y1}) -> ({x2},{y2})  [{x2-x1}x{y2-y1}px]")
    
    patch_result, n_px = inpaint_region(arr, x1, y1, x2, y2)
    arr[y1:y2, x1:x2] = patch_result
    
    print(f"  Pixels modificados (blend>5%): {n_px}")
    
    result_img = Image.fromarray(arr)
    result_img.save(out_path, format="PNG", optimize=False)
    print(f"  [OK] Guardado: {out_path.name}")


def main():
    images = sorted([
        p for p in OFICIALES_DIR.glob("*.png")
        if "without watermark" not in p.stem.lower()
    ])
    print(f"Imagenes a procesar: {len(images)}")
    
    for img_path in images:
        out_path = img_path.parent / f"{img_path.stem} without watermark.png"
        process_image(img_path, out_path)
    
    print("\n[DONE] Proceso completado.")


if __name__ == "__main__":
    main()
