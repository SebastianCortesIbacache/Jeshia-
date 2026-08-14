import os
from PIL import Image

# Configuración
DPI = 300
MM_TO_PX = DPI / 25.4
CANVAS_SIZE_MM = 1000
CANVAS_SIZE_PX = int(CANVAS_SIZE_MM * MM_TO_PX) # ~11811 px
GAP_MM = 2
GAP_PX = int(GAP_MM * MM_TO_PX)

# El ancho objetivo para el bloque será de 930mm (exactamente 15 etiquetas de 60mm + márgenes)
BLOCK_WIDTH_MM = 930
BLOCK_WIDTH_PX = int(BLOCK_WIDTH_MM * MM_TO_PX)

BASE_DIR = r"e:\Logo Jeshia\etiquetas_impresion"

aromas_main = ["berries", "coco_nut", "citric", "sugar", "chicle"]
aromas_other = ["lavanda", "vainilla_coco", "manzana_canela", "frutal_mango", "pino"]

# Definir la lista de requerimientos
requirements = [
    {
        "folder": "02_Home_Spray_60x75mm",
        "prefix": "Home_Spray",
        "width_mm": 60,
        "height_mm": 75,
        "counts": {**{a: 20 for a in aromas_main}, **{a: 2 for a in aromas_other}} # +10 nuevos
    },
    {
        "folder": "05_Recarga_500ml_60x100mm",
        "prefix": "Recarga_500ml",
        "width_mm": 60,
        "height_mm": 100,
        "counts": {**{a: 2 for a in aromas_main}, **{a: 1 for a in aromas_other}}
    },
    {
        "folder": "04_Recarga_250ml_60x75mm",
        "prefix": "Recarga_250ml",
        "width_mm": 60,
        "height_mm": 75,
        "counts": {**{a: 2 for a in aromas_main}, **{a: 1 for a in aromas_other}}
    },
    {
        "folder": "01_Mikado_50x25mm",
        "prefix": "Mikado",
        "width_mm": 50,
        "height_mm": 25,
        "counts": {**{a: 2 for a in aromas_main}, **{a: 1 for a in aromas_other}}
    },
    {
        "folder": "03_Aromatizador_Redonda_Ovalada",
        "prefix": "Aromatizador",
        "width_mm": 20,
        "height_mm": 20,
        "counts": {**{a: 2 for a in aromas_main}, **{a: 1 for a in aromas_other}}
    }
]

print("Cargando imágenes...")
items_to_pack = []

# Recolectar todas las imágenes
for req in requirements:
    w_px = int(req["width_mm"] * MM_TO_PX)
    h_px = int(req["height_mm"] * MM_TO_PX)
    
    for aroma, count in req["counts"].items():
        if count <= 0:
            continue
            
        img_path = os.path.join(BASE_DIR, req["folder"], f"{req['prefix']}_{aroma}.png")
        if not os.path.exists(img_path):
            print(f"Advertencia: No se encontró la imagen {img_path}")
            continue
            
        try:
            with Image.open(img_path) as img:
                img = img.convert("RGBA")
                img = img.resize((w_px, h_px), Image.Resampling.LANCZOS)
                
                for _ in range(count):
                    items_to_pack.append({
                        "img": img,
                        "w": w_px,
                        "h": h_px
                    })
        except Exception as e:
            print(f"Error al cargar {img_path}: {e}")

print(f"Total de etiquetas cargadas: {len(items_to_pack)}")

# Ordenar por altura para guillotina
items_to_pack.sort(key=lambda item: item["h"], reverse=True)

# Simular el empaquetado para calcular el tamaño real del bloque (con la lógica de guillotina)
def simulate_packing(items, max_width_px, gap_px):
    x, y = 0, 0
    max_x = 0
    current_shelf_height = 0
    
    for item in items:
        if (x + item["w"] > max_width_px and x > 0) or (current_shelf_height > 0 and item["h"] != current_shelf_height):
            y += current_shelf_height + gap_px
            x = 0
            current_shelf_height = 0
            
        actual_x = x + item["w"]
        if actual_x > max_x:
            max_x = actual_x
            
        current_shelf_height = max(current_shelf_height, item["h"])
        x += item["w"] + gap_px
        
    total_y = y + current_shelf_height
    return max_x, total_y

print("Calculando empaquetado y centrando...")
block_w, block_h = simulate_packing(items_to_pack, BLOCK_WIDTH_PX, GAP_PX)
print(f"Dimensiones del bloque interior: {block_w / MM_TO_PX:.1f} mm de ancho x {block_h / MM_TO_PX:.1f} mm de alto")

# Calcular punto de inicio para repartir el espacio sobrante en los 4 bordes (centrado)
start_x = (CANVAS_SIZE_PX - block_w) // 2
start_y = (CANVAS_SIZE_PX - block_h) // 2

print(f"Creando lienzo blanco de {CANVAS_SIZE_PX}x{CANVAS_SIZE_PX} píxeles (1x1 metro a 300 DPI)...")
canvas = Image.new("RGB", (CANVAS_SIZE_PX, CANVAS_SIZE_PX), "white")

print("Dibujando etiquetas en el lienzo...")
x, y = start_x, start_y
current_shelf_height = 0

for item in items_to_pack:
    # Forzar nueva fila si excede el ancho, o si la altura cambia
    if (x + item["w"] > start_x + BLOCK_WIDTH_PX and x > start_x) or (current_shelf_height > 0 and item["h"] != current_shelf_height):
        y += current_shelf_height + GAP_PX
        x = start_x
        current_shelf_height = 0
    
    canvas.paste(item["img"], (x, y), item["img"])
    
    current_shelf_height = max(current_shelf_height, item["h"])
    x += item["w"] + GAP_PX

output_png = os.path.join(BASE_DIR, "lienzo_impresion_1x1m_v4.png")
output_pdf = os.path.join(BASE_DIR, "lienzo_impresion_1x1m_v4.pdf")

print(f"Guardando {output_png}...")
canvas.save(output_png, dpi=(DPI, DPI))

print(f"Guardando {output_pdf}...")
canvas.save(output_pdf, "PDF", resolution=DPI)

print("¡Proceso completado con éxito!")
