import os
from PIL import Image, ImageDraw
from collections import defaultdict

# Configuración
DPI = 300
MM_TO_PX = DPI / 25.4
PAGE_WIDTH_MM = 279.4  # 11 pulgadas
PAGE_HEIGHT_MM = 431.8 # 17 pulgadas
MARGIN_MM = 10         # Margen de impresión
GAP_MM = 2

PAGE_WIDTH_PX = int(PAGE_WIDTH_MM * MM_TO_PX)
PAGE_HEIGHT_PX = int(PAGE_HEIGHT_MM * MM_TO_PX)
MARGIN_PX = int(MARGIN_MM * MM_TO_PX)
GAP_PX = int(GAP_MM * MM_TO_PX)

USABLE_WIDTH_PX = PAGE_WIDTH_PX - 2 * MARGIN_PX
USABLE_HEIGHT_PX = PAGE_HEIGHT_PX - 2 * MARGIN_PX

BASE_DIR = r"e:\Logo Jeshia\etiquetas_impresion"
OUT_DIR = os.path.join(BASE_DIR, "Archivos_Listos_Impresion")
os.makedirs(OUT_DIR, exist_ok=True)

aromas = ["berries", "coco_nut", "citric", "sugar", "chicle"]

# Definir la lista de requerimientos
requirements = [
    {
        "folder": "02_Home_Spray_60x75mm",
        "prefix": "Home_Spray",
        "width_mm": 60,
        "height_mm": 75,
        "count_per_aroma": 10
    },
    {
        "folder": "01_Mikado_50x25mm",
        "prefix": "Mikado",
        "width_mm": 50,
        "height_mm": 25,
        "count_per_aroma": 2
    },
    {
        "folder": "03_Aromatizador_Redonda_Ovalada",
        "prefix": "Aromatizador",
        "width_mm": 20,
        "height_mm": 20,
        "count_per_aroma": 2
    },
    {
        "folder": "04_Recarga_250ml_60x75mm",
        "prefix": "Recarga_250ml",
        "width_mm": 60,
        "height_mm": 75,
        "count_per_aroma": 2
    },
    {
        "folder": "05_Recarga_500ml_60x100mm",
        "prefix": "Recarga_500ml",
        "width_mm": 60,
        "height_mm": 100,
        "count_per_aroma": 2
    }
]

print("Cargando imágenes...")
items_to_pack = []

for req in requirements:
    w_px = int(req["width_mm"] * MM_TO_PX)
    h_px = int(req["height_mm"] * MM_TO_PX)
    
    for aroma in aromas:
        count = req["count_per_aroma"]
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
                        "h": h_px,
                        "group": f"{req['width_mm']}x{req['height_mm']}"
                    })
        except Exception as e:
            print(f"Error al cargar {img_path}: {e}")

print(f"Total de etiquetas cargadas: {len(items_to_pack)}")

# Agrupar por tamaño exacto para asegurar que queden en cuadrículas perfectas (cortes fáciles)
grouped_items = defaultdict(list)
for item in items_to_pack:
    grouped_items[(item["w"], item["h"])].append(item)

pages = []
current_page_items = []
current_y = 0

for (w, h), items in grouped_items.items():
    cols = USABLE_WIDTH_PX // (w + GAP_PX)
    if cols == 0: cols = 1
    
    col = 0
    # Si no cabe ni una sola fila en la página actual, pasamos a la siguiente
    if current_y + h > USABLE_HEIGHT_PX:
        pages.append(current_page_items)
        current_page_items = []
        current_y = 0

    for item in items:
        if col >= cols:
            col = 0
            current_y += h + GAP_PX
            # Verificamos si la nueva fila cabe
            if current_y + h > USABLE_HEIGHT_PX:
                pages.append(current_page_items)
                current_page_items = []
                current_y = 0
                
        current_page_items.append({
            "img": item["img"],
            "x": MARGIN_PX + col * (w + GAP_PX),
            "y": MARGIN_PX + current_y,
            "w": w,
            "h": h
        })
        col += 1
        
    # Al finalizar un bloque de tamaño uniforme, avanzamos 'y' para el siguiente bloque
    # De esta manera la guillotina puede hacer un corte horizontal limpio entre tamaños
    if col > 0:
        current_y += h + GAP_PX

# Añadir la última página
if current_page_items:
    pages.append(current_page_items)

print(f"Total de páginas a generar: {len(pages)}")

page_images = []

for i, page_items in enumerate(pages):
    print(f"Generando página {i+1}...")
    canvas = Image.new("RGB", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), "white")
    draw = ImageDraw.Draw(canvas)
    
    for item in page_items:
        # Pegar la imagen
        canvas.paste(item["img"], (item["x"], item["y"]), item["img"])
        
        # Dibujar guías de corte en los bordes de la página (fuera del margen de impresión)
        # Esto hace el trabajo de guillotina mucho más preciso y fácil
        tick_len = MARGIN_PX // 2
        
        # Guías horizontales (izquierda)
        draw.line([(0, item["y"]), (tick_len, item["y"])], fill="#CCCCCC", width=1)
        draw.line([(0, item["y"] + item["h"]), (tick_len, item["y"] + item["h"])], fill="#CCCCCC", width=1)
        
        # Guías horizontales (derecha)
        draw.line([(PAGE_WIDTH_PX - tick_len, item["y"]), (PAGE_WIDTH_PX, item["y"])], fill="#CCCCCC", width=1)
        draw.line([(PAGE_WIDTH_PX - tick_len, item["y"] + item["h"]), (PAGE_WIDTH_PX, item["y"] + item["h"])], fill="#CCCCCC", width=1)
        
        # Guías verticales (arriba)
        draw.line([(item["x"], 0), (item["x"], tick_len)], fill="#CCCCCC", width=1)
        draw.line([(item["x"] + item["w"], 0), (item["x"] + item["w"], tick_len)], fill="#CCCCCC", width=1)
        
        # Guías verticales (abajo)
        draw.line([(item["x"], PAGE_HEIGHT_PX - tick_len), (item["x"], PAGE_HEIGHT_PX)], fill="#CCCCCC", width=1)
        draw.line([(item["x"] + item["w"], PAGE_HEIGHT_PX - tick_len), (item["x"] + item["w"], PAGE_HEIGHT_PX)], fill="#CCCCCC", width=1)

    page_images.append(canvas)
    
    output_png = os.path.join(OUT_DIR, f"impresion_doble_carta_pag_{i+1}.png")
    print(f"Guardando {output_png}...")
    canvas.save(output_png, dpi=(DPI, DPI))

output_pdf = os.path.join(OUT_DIR, "impresion_doble_carta_completo.pdf")
print(f"Guardando {output_pdf}...")
if page_images:
    page_images[0].save(
        output_pdf, "PDF", resolution=DPI, save_all=True, append_images=page_images[1:]
    )

print("¡Proceso completado con éxito!")
