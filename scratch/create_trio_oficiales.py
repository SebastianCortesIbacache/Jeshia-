import os
from PIL import Image, ImageOps, ImageFilter

p_spray = 'assets/montajes/oficiales/Home Spray Sin Marca.png'
p_mikado = 'assets/montajes/oficiales/Mikado Sin Marca.png'
p_recarga = 'assets/montajes/oficiales/Recarga 250 Sin Marca 2.png'

im_spray = Image.open(p_spray).convert('RGBA')
im_mikado = Image.open(p_mikado).convert('RGBA')
im_recarga = Image.open(p_recarga).convert('RGBA')

# Target composite width 1080, height 640
# Let's crop each product tightly around the bottle + reeds/trigger + shadow
# 1. Mikado: (780, 140, 1620, 1480) -> size (840, 1340)
crop_mik = im_mikado.crop((780, 140, 1620, 1480))
# 2. Spray: (860, 60, 1580, 1540) -> size (720, 1480)
crop_spr = im_spray.crop((860, 60, 1580, 1540))
# 3. Recarga 250: (920, 100, 1480, 1520) -> size (560, 1420)
crop_rec = im_recarga.crop((920, 100, 1480, 1520))

# Resize to proportional heights on our 640px high canvas
# Let's see: Spray height ~ 540px, Mikado height ~ 510px, Recarga height ~ 510px
th_spray = 540
tw_spray = int(crop_spr.width * (th_spray / crop_spr.height))
r_spray = crop_spr.resize((tw_spray, th_spray), Image.Resampling.LANCZOS)

th_mik = 510
tw_mik = int(crop_mik.width * (th_mik / crop_mik.height))
r_mik = crop_mik.resize((tw_mik, th_mik), Image.Resampling.LANCZOS)

th_rec = 500
tw_rec = int(crop_rec.width * (th_rec / crop_rec.height))
r_rec = crop_rec.resize((tw_rec, th_rec), Image.Resampling.LANCZOS)

# Create 3-panel editorial container or blended stage
canvas_w, canvas_h = 1080, 640
canvas = Image.new('RGBA', (canvas_w, canvas_h), (251, 248, 243, 255))

# Let's create a 3-panel cards presentation or composite side-by-side
# Panel widths: 350px each with 10px spacing
panel_w = 340
panel_h = 580
y_offset = 30

for i, (img, name) in enumerate([(r_mik, "Mikado 50ml"), (r_spray, "Home Spray 250ml"), (r_rec, "Recarga Eco 250ml")]):
    panel = Image.new('RGBA', (panel_w, panel_h), (255, 255, 255, 200))
    # Paste centered in panel
    px = (panel_w - img.width) // 2
    py = (panel_h - img.height) // 2
    panel.paste(img, (px, py), img)
    
    canvas_x = 25 + i * (panel_w + 15)
    canvas.paste(panel, (canvas_x, y_offset), panel)

out_trio = 'visuales/set_ritual_trio_oficiales.png'
canvas.save(out_trio)
print(f"Saved trio composite to {out_trio}")
