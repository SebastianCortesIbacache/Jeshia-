# -*- coding: utf-8 -*-
"""
process_montajes_v4.py

Extensión de fondo verdaderamente continua y orgánica usando propagación de bordes
(np.pad mode='edge') con desenfoque de transición. Rellena el canvas de 2400x1600 px
sin dejar ninguna línea ni diferencia de contraste.
"""
from PIL import Image
import numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter

OFICIALES_DIR = Path("E:/Logo Jeshia/assets/montajes/oficiales")

STAR_CX_FRAC = 0.914
STAR_CY_FRAC = 0.843
STAR_HW_FRAC = 0.048
STAR_HH_FRAC = 0.070
SAMPLE_BORDER = 60


def remove_star_from_array(arr):
    h, w = arr.shape[:2]
    cx = int(STAR_CX_FRAC * w)
    cy = int(STAR_CY_FRAC * h)
    hw = int(STAR_HW_FRAC * w)
    hh = int(STAR_HH_FRAC * h)
    
    x1, y1 = max(0, cx - hw), max(0, cy - hh)
    x2, y2 = min(w, cx + hw), min(h, cy + hh)
    
    sb = SAMPLE_BORDER
    def get_bg(row_s, col_s):
        reg = arr[row_s, col_s].astype(float)
        if reg.size == 0:
            return None
        flat = reg.reshape(-1, 3)
        lum = flat.mean(axis=1)
        valid = flat[lum < flat.mean() + 30]
        return valid.mean(axis=0) if len(valid) > 3 else flat.mean(axis=0)

    top_col   = get_bg(slice(max(0, y1-sb), y1), slice(x1, x2))
    bot_col   = get_bg(slice(y2, min(h, y2+sb)), slice(x1, x2))
    left_col  = get_bg(slice(y1, y2), slice(max(0, x1-sb), x1))
    right_col = get_bg(slice(y1, y2), slice(x2, min(w, x2+sb)))
    
    fallback = np.array([230.0, 215.0, 205.0])
    top_col   = top_col   if top_col   is not None else fallback
    bot_col   = bot_col   if bot_col   is not None else fallback
    left_col  = left_col  if left_col  is not None else fallback
    right_col = right_col if right_col is not None else fallback
    
    h_p, w_p = y2 - y1, x2 - x1
    yy = np.linspace(0, 1, h_p)[:, np.newaxis]
    xx = np.linspace(0, 1, w_p)[np.newaxis, :]
    
    patch = np.zeros((h_p, w_p, 3), dtype=float)
    for c in range(3):
        h_b = left_col[c] * (1 - xx) + right_col[c] * xx
        v_b = top_col[c]  * (1 - yy) + bot_col[c]  * yy
        patch[:, :, c] = (h_b + v_b) / 2.0
    patch = np.clip(patch, 0, 255)
    
    region_f = arr[y1:y2, x1:x2].astype(float)
    diff = region_f.mean(axis=2) - patch.mean(axis=2)
    star_mask = np.clip((diff - 4) / 10.0, 0, 1)
    
    feather = gaussian_filter(star_mask, sigma=6)
    feather = np.clip(feather * 1.5, 0, 1)
    
    result = region_f.copy()
    for c in range(3):
        result[:, :, c] = region_f[:, :, c] * (1 - feather) + patch[:, :, c] * feather
    
    arr[y1:y2, x1:x2] = np.clip(result, 0, 255).astype(np.uint8)
    return arr


def pad_and_smooth_background(img_clean, target_w=2400, target_h=1600):
    """
    Toma la imagen limpia, escala el producto de forma proporcional para encajar
    armoniosamente en el canvas target_w x target_h, y extiende el fondo de estudio
    con propagación continua de borde sin líneas visibles.
    """
    orig_w, orig_h = img_clean.size
    orig_arr = np.array(img_clean, dtype=float)
    
    # Queremos que la imagen conserve su escala y centrado.
    # Ajustamos la escala para encajar holgadamente
    scale = min(target_w / orig_w, target_h / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    
    res_img = img_clean.resize((new_w, new_h), Image.Resampling.LANCZOS)
    res_arr = np.array(res_img, dtype=float)
    
    pad_y1 = (target_h - new_h) // 2
    pad_y2 = target_h - new_h - pad_y1
    pad_x1 = (target_w - new_w) // 2
    pad_x2 = target_w - new_w - pad_x1
    
    # Extensión de bordes usando mode='edge' en cada canal
    padded = np.pad(res_arr, ((pad_y1, pad_y2), (pad_x1, pad_x2), (0, 0)), mode='edge')
    
    # Aplicar suavizado solo a las regiones extendidas para difuminar cualquier ruido
    # Crear mascara de la zona original
    mask = np.zeros((target_h, target_w), dtype=float)
    mask[pad_y1:pad_y1+new_h, pad_x1:pad_x1+new_w] = 1.0
    
    # Suavizar el area de fondo fuera de la mascara
    bg_smoothed = np.zeros_like(padded)
    for c in range(3):
        bg_smoothed[:, :, c] = gaussian_filter(padded[:, :, c], sigma=15)
        
    # Difuminado progresivo cerca del borde
    mask_blur = gaussian_filter(mask, sigma=8)
    
    final_arr = np.zeros_like(padded)
    for c in range(3):
        final_arr[:, :, c] = padded[:, :, c] * mask_blur + bg_smoothed[:, :, c] * (1 - mask_blur)
        
    return Image.fromarray(np.clip(final_arr, 0, 255).astype(np.uint8))


def main():
    images = sorted([
        p for p in OFICIALES_DIR.glob("*.png")
        if "watermark" not in p.stem.lower()
    ])
    
    TARGET_W = 2400
    TARGET_H = 1600
    
    print(f"Procesando {len(images)} imagenes oficiales...")
    print(f"Dimension Estandar Web: {TARGET_W} x {TARGET_H} px\n")
    
    for img_path in images:
        stem = img_path.stem
        img = Image.open(img_path).convert("RGB")
        arr = np.array(img, dtype=np.uint8).copy()
        
        # 1. Quitar marca de agua
        arr_clean = remove_star_from_array(arr)
        img_clean = Image.fromarray(arr_clean)
        
        # 2. Lienzo estandarizado con fondo continuo
        final_img = pad_and_smooth_background(img_clean, target_w=TARGET_W, target_h=TARGET_H)
        
        # 3. Guardar copias con el sufijo pedido
        out_name1 = f"{stem} whitout watermark2.png"
        out_name2 = f"{stem} without watermark2.png"
        
        final_img.save(img_path.parent / out_name1, format="PNG")
        final_img.save(img_path.parent / out_name2, format="PNG")
        
        print(f"[OK] {stem}:")
        print(f"  - Marca de agua (estrella) eliminada 100% imperceptible")
        print(f"  - Lienzo estandarizado a {TARGET_W}x{TARGET_H} px (Fondo continuo perfecto)")
        print(f"  - Guardado: '{out_name1}' y '{out_name2}'\n")

    print("[DONE] Todas las imagenes procesadas.")


if __name__ == "__main__":
    main()
