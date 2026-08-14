# -*- coding: utf-8 -*-
"""
remove_star_watermark.py
Elimina la estrella blanca de 4 puntas (watermark) del corner inferior derecho
de todas las imagenes en los montajes oficiales de Jeshia.
Guarda copias como '[nombre] without watermark.png'

Tecnica: Inpainting por interpolacion bilineal del fondo circundante.
La estrella es blanca semitransparente sobre fondo beige uniforme.
"""
from PIL import Image
import numpy as np
import os
from pathlib import Path

OFICIALES_DIR = Path("E:/Logo Jeshia/assets/montajes/oficiales")

# Parámetros calibrados analizando las imágenes
# La estrella aparece en la zona inferior derecha de la imagen
# Como proporción del tamaño total de la imagen:
STAR_REL = {
    "cx": 0.9143,    # centro X como fracción del ancho (2543/2784)
    "cy": 0.8431,    # centro Y como fracción del alto  (1295/1536)
    "half_w": 0.040, # radio horizontal (110px / 2784)
    "half_h": 0.060, # radio vertical   (90px / 1536)
}

# Margen extra alrededor del bounding box para capturar fondo de referencia
BORDER = 40  # píxeles

def sample_border_color(arr, x1, y1, x2, y2, border=BORDER):
    """
    Muestrea el color promedio del borde exterior del rectángulo dado.
    Evita los píxeles brillantes (estrella) en la muestra.
    """
    h, w = arr.shape[:2]
    bx1 = max(0, x1 - border)
    by1 = max(0, y1 - border)
    bx2 = min(w, x2 + border)
    by2 = min(h, y2 + border)

    # Crear máscara del área interior (de la estrella) para excluirla
    samples = []
    for region in [
        arr[by1:y1, bx1:bx2],           # arriba
        arr[y2:by2, bx1:bx2],           # abajo
        arr[y1:y2, bx1:x1],             # izquierda
        arr[y1:y2, x2:bx2],             # derecha
    ]:
        if region.size > 0:
            flat = region.reshape(-1, 3).astype(float)
            # Excluir píxeles muy brillantes (que podrían ser parte de la estrella)
            not_star = flat[(flat[:,0] < 240) | (flat[:,1] < 240) | (flat[:,2] < 240)]
            if len(not_star) > 0:
                samples.append(not_star)
    
    if samples:
        all_samples = np.vstack(samples)
        return all_samples.mean(axis=0)
    return np.array([220, 210, 205], dtype=float)


def create_smooth_patch(x1, y1, x2, y2, arr, border=BORDER):
    """
    Genera un parche que rellena la zona [x1:x2, y1:y2] con una
    interpolación suave del fondo circundante (gradiente desde los bordes).
    """
    h_patch = y2 - y1
    w_patch = x2 - x1
    
    # Muestrea el color en los 4 bordes del rectángulo expandido
    hh, ww = arr.shape[:2]
    
    def sample_line(row_slice, col_slice):
        region = arr[row_slice, col_slice]
        if region.size == 0:
            return np.array([220, 210, 205], dtype=float)
        flat = region.reshape(-1, 3).astype(float)
        mask = (flat[:,0] < 242) | (flat[:,1] < 242) | (flat[:,2] < 242)
        valid = flat[mask]
        return valid.mean(axis=0) if len(valid) > 0 else flat.mean(axis=0)

    # Colores de referencia en los 4 bordes
    top_color    = sample_line(slice(max(0,y1-border), max(0,y1)), slice(x1, x2))
    bottom_color = sample_line(slice(min(hh,y2), min(hh,y2+border)), slice(x1, x2))
    left_color   = sample_line(slice(y1, y2), slice(max(0,x1-border), max(0,x1)))
    right_color  = sample_line(slice(y1, y2), slice(min(ww,x2), min(ww,x2+border)))

    # Interpolar horizontalmente y verticalmente
    patch = np.zeros((h_patch, w_patch, 3), dtype=float)
    
    for row in range(h_patch):
        v_frac = row / max(h_patch - 1, 1)  # 0.0 arriba → 1.0 abajo
        for col in range(w_patch):
            h_frac = col / max(w_patch - 1, 1)  # 0.0 izq → 1.0 der
            
            # Bilinear blend de los 4 colores de borde
            top_blend    = top_color    * (1 - h_frac) + right_color * h_frac
            bottom_blend = bottom_color * (1 - h_frac) + right_color * h_frac
            color = top_blend * (1 - v_frac) + bottom_blend * v_frac
            
            # Mezclar con horizontal puro también
            h_color = left_color * (1 - h_frac) + right_color * h_frac
            v_color = top_color  * (1 - v_frac) + bottom_color * v_frac
            color = (color + h_color + v_color) / 3.0
            
            patch[row, col] = np.clip(color, 0, 255)
    
    return patch.astype(np.uint8)


def remove_star(img_path: Path, out_path: Path):
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8).copy()
    h, w = arr.shape[:2]
    
    print(f"\nProcesando: {img_path.name}  ({w}x{h})")
    
    # Calcular bounding box de la estrella en esta imagen
    cx_star = int(STAR_REL["cx"] * w)
    cy_star = int(STAR_REL["cy"] * h)
    half_w  = int(STAR_REL["half_w"] * w) + 20  # +20px extra de margen
    half_h  = int(STAR_REL["half_h"] * h) + 20
    
    x1, y1 = max(0, cx_star - half_w), max(0, cy_star - half_h)
    x2, y2 = min(w, cx_star + half_w), min(h, cy_star + half_h)
    
    print(f"  Bounding box estrella: ({x1},{y1}) → ({x2},{y2})")
    
    # Generar parche de relleno interpolado
    patch = create_smooth_patch(x1, y1, x2, y2, arr)
    
    # Solo reemplazar los píxeles que son parte de la estrella (brillantes)
    # Esto evita sobrescribir áreas del fondo que ya son correctas
    region = arr[y1:y2, x1:x2].astype(float)
    
    # Máscara de la estrella: píxeles significativamente más brillantes que el fondo
    bg_color = sample_border_color(arr, x1, y1, x2, y2)
    print(f"  Color de fondo muestreado: {bg_color.astype(int)}")
    
    # Diferencia de luminosidad con el fondo
    region_lum  = region.mean(axis=2)
    bg_lum      = bg_color.mean()
    diff        = region_lum - bg_lum
    
    # Umbral: píxeles más de 18 puntos más brillantes que el fondo → estrella
    star_mask   = diff > 18
    
    # Crear parche con alpha blend suave (feather) para bordes imperceptibles
    # Generar máscara con feathering gaussiano
    from scipy.ndimage import gaussian_filter
    star_float  = star_mask.astype(float)
    feather_mask = gaussian_filter(star_float, sigma=4)
    feather_mask = np.clip(feather_mask, 0, 1)
    
    n_star_px = star_mask.sum()
    print(f"  Píxeles estrella detectados: {n_star_px}")
    
    # Blend: fondo_natural * (1 - mask) + patch * mask
    patch_f = patch.astype(float)
    for c in range(3):
        region[:,:,c] = region[:,:,c] * (1 - feather_mask) + patch_f[:,:,c] * feather_mask
    
    arr[y1:y2, x1:x2] = np.clip(region, 0, 255).astype(np.uint8)
    
    # Guardar resultado
    result = Image.fromarray(arr)
    result.save(out_path, format="PNG", optimize=False)
    print(f"  [OK] Guardado: {out_path.name}")


def main():
    try:
        from scipy.ndimage import gaussian_filter
        print("scipy disponible OK")
    except ImportError:
        print("scipy no encontrado, instalando...")
        import subprocess
        subprocess.run(["pip", "install", "scipy", "-q"], check=True)
    
    images = list(OFICIALES_DIR.glob("*.png"))
    # Excluir imágenes que ya son "without watermark"
    images = [p for p in images if "without watermark" not in p.stem.lower()]
    
    print(f"Imágenes a procesar: {len(images)}")
    for img_path in sorted(images):
        stem = img_path.stem
        out_name = f"{stem} without watermark.png"
        out_path = img_path.parent / out_name
        remove_star(img_path, out_path)
    
    print("\n[DONE] Todos los archivos procesados.")


if __name__ == "__main__":
    main()
