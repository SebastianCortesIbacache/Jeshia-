import os
import subprocess
import base64
import shutil
from PIL import Image

# 1. Rutas a los envases oficiales
p_spray = 'assets/montajes/oficiales/Home Spray Sin Marca.png'
p_mikado = 'assets/montajes/oficiales/Mikado Sin Marca.png'
p_recarga = 'assets/montajes/oficiales/Recarga 250 Sin Marca 2.png'

# 2. Recorte centrado de cada envase oficial en alta resolución
im_spray = Image.open(p_spray).convert('RGB')
im_mikado = Image.open(p_mikado).convert('RGB')
im_recarga = Image.open(p_recarga).convert('RGB')

crop_mik = im_mikado.crop((760, 80, 1640, 1520))
crop_spr = im_spray.crop((820, 40, 1580, 1560))
crop_rec = im_recarga.crop((880, 60, 1520, 1540))

os.makedirs('visuales/oficiales_crops', exist_ok=True)
crop_mik_path = 'visuales/oficiales_crops/mikado_oficial.jpg'
crop_spr_path = 'visuales/oficiales_crops/spray_oficial.jpg'
crop_rec_path = 'visuales/oficiales_crops/recarga_oficial.jpg'

crop_mik.save(crop_mik_path, quality=96)
crop_spr.save(crop_spr_path, quality=96)
crop_rec.save(crop_rec_path, quality=96)

def get_b64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    ext = path.split('.')[-1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/webp'
    with open(path, 'rb') as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')

mik_b64 = get_b64(crop_mik_path)
spr_b64 = get_b64(crop_spr_path)
rec_b64 = get_b64(crop_rec_path)
logo_b64 = get_b64("assets/logos/Jeshia Colores_Transparent.png")

# 3. Leer la plantilla HTML y reemplazar las variables base64
template_path = "set_ritual_oficiales_mkt.html"
if os.path.exists(template_path):
    with open(template_path, "r", encoding="utf-8") as f:
        html_data = f.read()
    
    # Reemplazos dinámicos
    html_data = html_data.replace("__MIK_B64__", mik_b64)
    html_data = html_data.replace("__SPR_B64__", spr_b64)
    html_data = html_data.replace("__REC_B64__", rec_b64)
    html_data = html_data.replace("__LOGO_B64__", logo_b64)
    
    rendered_html_path = "scratch/set_ritual_rendered.html"
    os.makedirs("scratch", exist_ok=True)
    with open(rendered_html_path, "w", encoding="utf-8") as f:
        f.write(html_data)
else:
    print(f"[ERROR] Template {template_path} not found.")
    exit(1)

# 4. Renderizar a imagen 1080x1350 px mediante Microsoft Edge Headless
edge_bin = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
abs_html = os.path.abspath(rendered_html_path).replace('\\', '/')
primary_out = os.path.abspath('visuales/set_ritual_mkt_4x5.png')

if os.path.exists(primary_out):
    os.remove(primary_out)

cmd = [
    edge_bin,
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    '--window-size=1080,1350',
    '--virtual-time-budget=3500',
    f'--screenshot={primary_out}',
    f'file:///{abs_html}'
]

print("Rendering Official Set Ritual Ad Poster (1080x1350)...")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(primary_out):
    print(f"[OK] Rendered {primary_out} ({os.path.getsize(primary_out)} bytes)")
    os.makedirs('assets/visuales', exist_ok=True)
    shutil.copy2(primary_out, 'assets/visuales/set_ritual_mkt_4x5.png')
    print("[OK] Saved copy to assets/visuales/set_ritual_mkt_4x5.png")
else:
    print(f"[ERROR] Rendering failed: {res.stderr}")
