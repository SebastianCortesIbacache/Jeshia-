# -*- coding: utf-8 -*-
"""
process_montajes_v2.py

1. Elimina la estrella blanca (watermark) del corner inferior derecho de forma imperceptible.
2. Estandariza TODAS las imagenes al MISMO alto y ancho (por ej. 2400 x 1600 px o 2000 x 1500 px o 1920 x 1080 px).
3. Ajusta el lienzo extendiendo suavemente el fondo sin deformar ni recortar el producto.
4. Guarda las copias como '[Nombre] whitout watermark2.png' y '[Nombre] without watermark2.png' en E:/Logo Jeshia/assets/montajes/oficiales.
"""
from PIL import Image
import numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter

OFICIALES_DIR = Path("E:/Logo Jeshia/assets/montajes/oficiales")

# Coordenadas relativas de la estrella
STAR_CX_FRAC = 0.914
STAR_CY_FRAC = 0.843
STAR_HW_FRAC = 0.048
STAR_HH_FRAC = 0.070
SAMPLE_BORDER = 60


def remove_star_from_array(arr):
    """Elimina la estrella de la esquina inferior derecha en un ndarray RGB."""
    h, w = arr.shape[:2]
    cx = int(STAR_CX_FRAC * w)
    cy = int(STAR_CY_FRAC * h)
    hw = int(STAR_HW_FRAC * w)
    hh = int(STAR_HH_FRAC * h)
    
    x1, y1 = max(0, cx - hw), max(0, cy - hh)
    x2, y2 = min(w, cx + hw), min(h, cy + hh)
    
    # Muestreo de fondo
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


def standardize_canvas(img_clean, target_w=2400, target_h=1600):
    """
    Coloca la imagen limpia sobre un lienzo unificado de target_w x target_h.
    Si la imagen original difiere de la proporcion del lienzo, escala manteniendo
    proporcion y extiende suavemente el fondo en los bordes.
    """
    orig_w, orig_h = img_clean.size
    target_ratio = target_w / target_h
    orig_ratio = orig_w / orig_h
    
    # Decidir escala para ajustar sin deformar
    if orig_ratio > target_ratio:
        # La imagen original es mas ancha relativemente -> ajustar por ancho o por alto de forma que llene el lienzo adecuadamente
        # Queremos mantener todo el producto visible
        scale = min(target_w / orig_w, target_h / orig_h)
    else:
        scale = min(target_w / orig_w, target_h / orig_h)
        
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    
    resized = img_clean.resize((new_w, new_h), Image.Resampling.LANCZOS)
    res_arr = np.array(resized)
    
    # Crear el lienzo final
    canvas = np.zeros((target_h, target_w, 3), dtype=float)
    
    # Posicion centrada
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    
    # Colocar la imagen en el centro
    canvas[offset_y:offset_y+new_h, offset_x:offset_x+new_w] = res_arr.astype(float)
    
    # Muestrear los bordes de la imagen escalada para rellenar las franjas de fondo
    top_edge = res_arr[0:5, :, :].mean(axis=(0,1))
    bot_edge = res_arr[-5:, :, :].mean(axis=(0,1))
    left_edge = res_arr[:, 0:5, :].mean(axis=(0,1))
    right_edge = res_arr[:, -5:, :].mean(axis=(0,1))
    
    # Rellenar zonas vacias (arriba, abajo, izquierda, derecha) si existen
    if offset_y > 0:
        for y in range(offset_y):
            canvas[y, offset_x:offset_x+new_w] = top_edge
        for y in range(offset_y+new_h, target_h):
            canvas[y, offset_x:offset_x+new_w] = bot_edge
            
    if offset_x > 0:
        for x in range(offset_x):
            canvas[:, x] = left_edge
        for x in range(offset_x+new_w, target_w):
            canvas[:, x] = right_edge
            
    # Rellenar esquinas si quedaron vacias
    if offset_y > 0 and offset_x > 0:
        canvas[0:offset_y, 0:offset_x] = (top_edge + left_edge) / 2.0
        canvas[0:offset_y, offset_x+new_w:target_w] = (top_edge + right_edge) / 2.0
        canvas[offset_y+new_h:target_h, 0:offset_x] = (bot_edge + left_edge) / 2.0
        canvas[offset_y+new_h:target_h, offset_x+new_w:target_w] = (bot_edge + right_edge) / 2.0

    # Aplicar un suave gaussian blur a las zonas de relleno para transicion perfecta
    canvas_img = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    return canvas_img


def main():
    images = sorted([
        p for p in OFICIALES_DIR.glob("*.png")
        if "watermark" not in p.stem.lower()
    ])
    
    # Dimension estandar recomendada para web: 2400 x 1600 px (3:2) o 2000 x 1500 px (4:3)
    TARGET_W = 2400
    TARGET_H = 1600
    
    print(f"Procesando {len(images)} imagenes oficiales...")
    print(f"Dimension Web Estandar: {TARGET_W} x {TARGET_H} px\n")
    
    for img_path in images:
        stem = img_path.stem
        img = Image.open(img_path).convert("RGB")
        arr = np.array(img, dtype=np.uint8).copy()
        
        # 1. Eliminar marca de agua
        arr_clean = remove_star_from_array(arr)
        img_clean = Image.fromarray(arr_clean)
        
        # 2. Estandarizar dimensiones al mismo ancho y alto para web
        final_img = standardize_canvas(img_clean, target_w=TARGET_W, target_h=TARGET_H)
        
        # 3. Guardar con el nombre solicitado
        out_name1 = f"{stem} whitout watermark2.png"
        out_name2 = f"{stem} without watermark2.png"
        
        out_path1 = img_path.parent / out_name1
        out_path2 = img_path.parent / out_name2
        
        final_img.save(out_path1, format="PNG", optimize=False)
        final_img.save(out_path2, format="PNG", optimize=False)
        
        print(f"[OK] {stem}:")
        print(f"  - Marca de agua eliminada imperceptiblemente")
        print(f"  - Formato estandarizado a {TARGET_W}x{TARGET_H} px")
        print(f"  - Guardado como: '{out_name1}' y '{out_name2}'\n")

    print("[DONE] Todas las imagenes procesadas con exito.")


if __name__ == "__main__":
    main()
