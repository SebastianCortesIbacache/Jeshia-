"""
Jeshia — Generador Oficial de Capas de Reserva Spot UV / Foil Dorado (K:100% Mask)
Genera las máscaras monocromáticas requeridas por la imprenta para aplicar barniz sectorizado o estampado en caliente (foil) sobre el logo y marcos de Jeshia.
"""

import os
from PIL import Image, ImageOps, ImageEnhance

BASE_DIR = r"e:\Logo Jeshia\etiquetas_impresion"
OUT_DIR = os.path.join(BASE_DIR, "Archivos_Listos_Impresion", "Capas_Spot_UV")
os.makedirs(OUT_DIR, exist_ok=True)

def generate_spot_uv_mask(img_path, output_path, threshold=200):
    """
    Convierte una etiqueta en su máscara Spot UV (K: 100%).
    Las áreas donde irá el barniz brillante/foil se transforman en negro puro (0,0,0)
    y el fondo queda en blanco puro (255,255,255) o transparente.
    """
    if not os.path.exists(img_path):
        print(f"Archivo no encontrado: {img_path}")
        return False
        
    with Image.open(img_path) as img:
        img = img.convert("RGBA")
        
        # Crear máscara basada en luminosidad / canal alfa
        # Los elementos oscuros (texto, logo, bordes) se vuelven negro K:100%
        gray = img.convert("L")
        
        # Binarización para obtener contornos nítidos al 100% K
        # En escala de grises: 0 es negro (logo/texto), 255 es fondo claro
        mask = gray.point(lambda p: 255 if p > threshold else 0)
        
        # Invertir para que lo que se barniza sea negro K y el fondo blanco
        # En especificación de imprenta: Negro K = 100% barniz, Blanco = 0% barniz
        spot_uv_layer = ImageOps.invert(mask)
        
        spot_uv_layer.save(output_path, "PNG", dpi=(300, 300))
        print(f"[OK] Mascara Spot UV generada: {os.path.basename(output_path)}")
        return True

if __name__ == "__main__":
    print("Iniciando generacion de mascaras de prueba Spot UV...")
    sample_img = os.path.join(BASE_DIR, "01_Mikado_50x25mm", "Mikado_mokka.png")
    sample_out = os.path.join(OUT_DIR, "Mikado_mokka_SpotUV_K100.png")
    if os.path.exists(sample_img):
        generate_spot_uv_mask(sample_img, sample_out)
