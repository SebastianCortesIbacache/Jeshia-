"""
Jeshia — Generador Oficial de Pliegos de Imprenta con Sangrado (Bleed 2mm) y Guías de Corte
Garantiza que ningún corte de guillotina deje bordes blancos no deseados.
"""

import os
from PIL import Image, ImageDraw

DPI = 300
MM_TO_PX = DPI / 25.4

# Dimensiones de Pliego Estándar Doble Carta (11x17 pulgadas)
PAGE_WIDTH_MM = 279.4
PAGE_HEIGHT_MM = 431.8
MARGIN_MM = 10
BLEED_MM = 2.0   # Sangrado de 2mm por lado
GAP_MM = 3.0     # Espacio entre etiquetas con sangrado

PAGE_WIDTH_PX = int(PAGE_WIDTH_MM * MM_TO_PX)
PAGE_HEIGHT_PX = int(PAGE_HEIGHT_MM * MM_TO_PX)
MARGIN_PX = int(MARGIN_MM * MM_TO_PX)
BLEED_PX = int(BLEED_MM * MM_TO_PX)
GAP_PX = int(GAP_MM * MM_TO_PX)

BASE_DIR = r"e:\Logo Jeshia\etiquetas_impresion"
OUT_DIR = os.path.join(BASE_DIR, "Archivos_Listos_Impresion")
os.makedirs(OUT_DIR, exist_ok=True)

def add_bleed_and_crop_marks(img, original_w_px, original_h_px, bleed_px):
    """Extiende los bordes de la imagen para crear el sangrado y añade marcas de corte."""
    total_w = original_w_px + 2 * bleed_px
    total_h = original_h_px + 2 * bleed_px
    
    # Crear lienzo con sangrado extendiendo bordes (edge replication)
    bleed_img = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))
    bleed_img.paste(img.resize((total_w, total_h), Image.Resampling.LANCZOS), (0, 0))
    bleed_img.paste(img, (bleed_px, bleed_px), img if img.mode == 'RGBA' else None)
    
    # Dibujar líneas guía sutiles de corte en las esquinas
    draw = ImageDraw.Draw(bleed_img)
    mark_len = int(3 * MM_TO_PX)
    mark_color = (180, 180, 180, 200)
    
    # Esquinas superiores
    draw.line([(0, bleed_px), (mark_len, bleed_px)], fill=mark_color, width=1)
    draw.line([(bleed_px, 0), (bleed_px, mark_len)], fill=mark_color, width=1)
    draw.line([(total_w - mark_len, bleed_px), (total_w, bleed_px)], fill=mark_color, width=1)
    draw.line([(total_w - bleed_px, 0), (total_w - bleed_px, mark_len)], fill=mark_color, width=1)
    
    # Esquinas inferiores
    draw.line([(0, total_h - bleed_px), (mark_len, total_h - bleed_px)], fill=mark_color, width=1)
    draw.line([(bleed_px, total_h - mark_len), (bleed_px, total_h)], fill=mark_color, width=1)
    draw.line([(total_w - mark_len, total_h - bleed_px), (total_w, total_h - bleed_px)], fill=mark_color, width=1)
    draw.line([(total_w - bleed_px, total_h - mark_len), (total_w - bleed_px, total_h)], fill=mark_color, width=1)
    
    return bleed_img

print("✓ Módulo de Pliegos con Sangrado (Bleed 2mm) configurado exitosamente.")
