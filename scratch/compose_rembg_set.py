import os
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np

# Background scene (high-res living room with gift box on travertine tray)
bg_path = r"C:\Users\Wusch\.gemini\antigravity-ide\brain\578ab548-d975-4692-bc32-38b3e2339992\clean_set_ritual_box_1786923237084.jpg"
bg = Image.open(bg_path).convert('RGBA')

# Cutouts from rembg, tightly cropped
cut_spray = Image.open('scratch/rembg_oficiales/spray_cut.png').convert('RGBA').crop(Image.open('scratch/rembg_oficiales/spray_cut.png').getbbox())
cut_mikado = Image.open('scratch/rembg_oficiales/mikado_cut.png').convert('RGBA').crop(Image.open('scratch/rembg_oficiales/mikado_cut.png').getbbox())
cut_recarga = Image.open('scratch/rembg_oficiales/recarga_cut.png').convert('RGBA').crop(Image.open('scratch/rembg_oficiales/recarga_cut.png').getbbox())

# Proportional scaling matching real 1:1 scale ratios:
# Home Spray (250ml) -> 17.5 cm
# Mikado (50ml) -> 7.0 cm glass + reeds
# Recarga (250ml) -> 17.5 cm
h_spray = 370
w_spray = int(cut_spray.width * (h_spray / cut_spray.height))
r_spr = cut_spray.resize((w_spray, h_spray), Image.Resampling.LANCZOS)

h_mik = 310
w_mik = int(cut_mikado.width * (h_mik / cut_mikado.height))
r_mik = cut_mikado.resize((w_mik, h_mik), Image.Resampling.LANCZOS)

h_rec = 340
w_rec = int(cut_recarga.width * (h_rec / cut_recarga.height))
r_rec = cut_recarga.resize((w_rec, h_rec), Image.Resampling.LANCZOS)

# Harmonic positions on the travertine tray floor in front of the gift box:
pos_spr = (215, 475)   # Base at y = 845
pos_mik = (315, 475)   # Base at y = 785
pos_rec = (395, 465)   # Base at y = 805

# Photorealistic Contact & Cast Shadows on Travertine Stone
def make_contact_shadow(width, height=9, opacity=0.65, blur=3.2):
    s = Image.new('RGBA', (width + 30, height + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    # Contact core
    d.ellipse((15, 10, 15 + width, 10 + height), fill=(30, 24, 18, int(255 * opacity)))
    return s.filter(ImageFilter.GaussianBlur(blur))

def make_directional_cast(img, offset_x=-8, offset_y=12, blur=10, opacity=0.22):
    a = img.split()[-1]
    s_mask = a.point(lambda p: int(p * opacity))
    s = Image.new('RGBA', img.size, (30, 25, 20, 255))
    s.putalpha(s_mask)
    return s.filter(ImageFilter.GaussianBlur(blur))

comp = bg.copy()

# Cast shadows (Light coming from top-right / window)
sh_mik = make_directional_cast(r_mik, offset_x=-6, offset_y=10, opacity=0.18, blur=9)
sh_rec = make_directional_cast(r_rec, offset_x=-6, offset_y=10, opacity=0.20, blur=9)
sh_spr = make_directional_cast(r_spr, offset_x=-8, offset_y=12, opacity=0.22, blur=10)

# 1. Mikado (Back center)
comp.paste(sh_mik, (pos_mik[0] - 6, pos_mik[1] + 10), sh_mik)
cs_mik = make_contact_shadow(r_mik.width - 25, height=8, opacity=0.60, blur=2.8)
comp.paste(cs_mik, (pos_mik[0] + 5, pos_mik[1] + h_mik - 6), cs_mik)
comp.paste(r_mik, pos_mik, r_mik)

# 2. Recarga Eco (Mid right, beside box)
comp.paste(sh_rec, (pos_rec[0] - 6, pos_rec[1] + 10), sh_rec)
cs_rec = make_contact_shadow(r_rec.width - 15, height=9, opacity=0.62, blur=2.8)
comp.paste(cs_rec, (pos_rec[0] + 2, pos_rec[1] + h_rec - 6), cs_rec)
comp.paste(r_rec, pos_rec, r_rec)

# 3. Home Spray (Front left)
comp.paste(sh_spr, (pos_spr[0] - 8, pos_spr[1] + 12), sh_spr)
cs_spr = make_contact_shadow(r_spr.width - 22, height=10, opacity=0.65, blur=3.0)
comp.paste(cs_spr, (pos_spr[0] + 3, pos_spr[1] + h_spray - 6), cs_spr)
comp.paste(r_spr, pos_spr, r_spr)

# Save final high-res composite image
out_comp = 'visuales/set_ritual_botanico_lifestyle_oficial.jpg'
comp.convert('RGB').save(out_comp, quality=97)
print(f"[OK] Perfect composite saved to {out_comp}")
