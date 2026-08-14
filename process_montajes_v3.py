# -*- coding: utf-8 -*-
"""
process_montajes_v3.py

Mejora de estandarización de lienzo (2400 x 1600 px):
Extensión de fondo studio ultra-suave y natural sin franjas visibles.
Utiliza gradiente bilineal adaptativo de bordes + mezcla gaussiana de textura.
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
    """Elimina la estrella de forma totalmente imperceptible."""
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


def extend_background_seamless(img_clean, target_w=2400, target_h=1600):
    """
    Extiende el fondo del estudio fotográfico sin recortar ni deformar el producto,
    creando una transición suave de gradiente de estudio en las dimensiones objetivo.
    """
    orig_w, orig_h = img_clean.size
    
    # Calcular escala para que el producto ocupe el tamaño perfecto en el centro
    scale_w = target_w / orig_w
    scale_h = target_h / orig_h
    
    # Queremos que la imagen se escale preservando la proporcion
    # Para la web, escalar para cubrir o contener de forma armonica
    # Si la diferencia de aspect ratio es pequeña, escalamos por el factor que mantiene todo el producto
    scale = min(scale_w, scale_h)
    
    # Si la imagen cabe dentro holgadamente, ajustamos escala
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    
    resized = img_clean.resize((new_w, new_h), Image.Resampling.LANCZOS)
    res_arr = np.array(resized, dtype=float)
    
    # Crear lienzo final
    canvas = np.zeros((target_h, target_w, 3), dtype=float)
    
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    
    # Muestrear gradiente vertical y horizontal del fondo de la imagen original
    # Arriba (background top), abajo (background bottom), izq, der
    bg_top = res_arr[0:15, :, :].mean(axis=(0,1))
    bg_bot = res_arr[-15:, :, :].mean(axis=(0,1))
    bg_left = res_arr[:, 0:15, :].mean(axis=(0,1))
    bg_right = res_arr[:, -15:, :].mean(axis=(0,1))
    
    # Construir lienzo con gradiente bilineal continuo
    yy = np.linspace(0, 1, target_h)[:, np.newaxis]
    xx = np.linspace(0, 1, target_w)[np.newaxis, :]
    
    for c in range(3):
        v_grad = bg_top[c] * (1 - yy) + bg_bot[c] * yy
        h_grad = bg_left[c] * (1 - xx) + bg_right[c] * xx
        canvas[:, :, c] = (v_grad + h_grad) / 2.0
    
    # Colocar la imagen en el centro con difuminado suave (feathering) en los bordes
    # Crear mascara de blend para integrar los bordes de res_arr en el gradiente del lienzo
    border_fade = 30 # px
    mask = np.ones((new_h, new_w), dtype=float)
    
    for i in range(border_fade):
        alpha = (i + 1) / border_fade
        mask[i, :] *= alpha
        mask[new_h - 1 - i, :] *= alpha
        mask[:, i] *= alpha
        mask[:, new_w - 1 - i] *= alpha
        
    mask = gaussian_filter(mask, sigma=3)
    
    # Mezclar res_arr sobre canvas
    y1, y2 = offset_y, offset_y + new_h
    x1, x2 = offset_x, offset_x + new_w
    
    for c in range(3):
        canvas[y1:y2, x1:x2, c] = res_arr[:, :, c] * mask + canvas[y1:y2, x1:x2, c] * (1 - mask)
        
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))


def main():
    images = sorted([
        p for p in OFICIALES_DIR.glob("*.png")
        if "watermark" not in p.stem.lower()
    ])
    
    TARGET_W = 2400
    TARGET_H = 1600
    
    print(f"Procesando {len(images)} imagenes oficiales...")
    print(f"Estandarizando a dimensiones Web: {TARGET_W} x {TARGET_H} px (Aspect Ratio 3:2)\n")
    
    for img_path in images:
        stem = img_path.stem
        img = Image.open(img_path).convert("RGB")
        arr = np.array(img, dtype=np.uint8).copy()
        
        # 1. Quitar marca de agua
        arr_clean = remove_star_from_array(arr)
        img_clean = Image.fromarray(arr_clean)
        
        # 2. Extender lienzo sin bordes visibles
        final_img = extend_background_seamless(img_clean, target_w=TARGET_W, target_h=TARGET_H)
        
        # 3. Guardar copias
        out_name1 = f"{stem} whitout watermark2.png"
        out_name2 = f"{stem} without watermark2.png"
        
        final_img.save(img_path.parent / out_name1, format="PNG")
        final_img.save(img_path.parent / out_name2, format="PNG")
        
        print(f"[OK] {stem}:")
        print(f"  - Marca de agua eliminada imperceptiblemente")
        print(f"  - Lienzo estandarizado de forma continua a {TARGET_W}x{TARGET_H} px")
        print(f"  - Guardado como: '{out_name1}' y '{out_name2}'\n")

    print("[DONE] Proceso completado exitosamente.")


if __name__ == "__main__":
    main()
