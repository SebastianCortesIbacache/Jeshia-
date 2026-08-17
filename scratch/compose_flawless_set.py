import os
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

# 1. Clean background with luxury gift box on travertine tray
bg_path = r"C:\Users\Wusch\.gemini\antigravity-ide\brain\578ab548-d975-4692-bc32-38b3e2339992\clean_set_ritual_box_1786923237084.jpg"
bg = Image.open(bg_path).convert('RGBA')
bw, bh = bg.size  # (896, 1200)

# 2. Extract precise cutouts of official bottles
def extract_bottle_flawless(img_path, box, tol=14):
    img = Image.open(img_path).convert('RGB')
    cropped = img.crop(box)
    arr = np.array(cropped).astype(np.float32)
    H, W, _ = arr.shape
    
    # Model vertical gradient background from outer borders
    left_profile = arr[:, :25, :].mean(axis=1)
    right_profile = arr[:, -25:, :].mean(axis=1)
    bg_profile = (left_profile + right_profile) / 2.0  # (H, 3)
    
    bg_model = np.repeat(bg_profile[:, np.newaxis, :], W, axis=1)
    dist = np.sqrt(np.sum((arr - bg_model)**2, axis=2))
    
    # Soft alpha ramp
    alpha = np.clip((dist - tol) / 6.0, 0, 1)
    alpha = (alpha * 255).astype(np.uint8)
    
    mask_img = Image.fromarray(alpha, mode='L')
    mask_img = mask_img.filter(ImageFilter.MedianFilter(3))
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(0.8))
    
    rgba = cropped.convert('RGBA')
    rgba.putalpha(mask_img)
    return rgba

p_spray = 'assets/montajes/oficiales/Home Spray Sin Marca.png'
p_mikado = 'assets/montajes/oficiales/Mikado Sin Marca.png'
p_recarga = 'assets/montajes/oficiales/Recarga 250 Sin Marca 2.png'

iso_spr = extract_bottle_flawless(p_spray, (820, 30, 1580, 1560), tol=12)
iso_mik = extract_bottle_flawless(p_mikado, (760, 60, 1640, 1490), tol=14)
iso_rec = extract_bottle_flawless(p_recarga, (880, 40, 1520, 1540), tol=12)

# 3. Proportional Scaling for the Travertine Tray Set:
# Home Spray (standing tall on left side of tray)
h_spray = 490
w_spray = int(iso_spr.width * (h_spray / iso_spr.height))
r_spr = iso_spr.resize((w_spray, h_spray), Image.Resampling.LANCZOS)

# Mikado (center of tray)
h_mik = 430
w_mik = int(iso_mik.width * (h_mik / iso_mik.height))
r_mik = iso_mik.resize((w_mik, h_mik), Image.Resampling.LANCZOS)

# Recarga Eco 250 (next to gift box)
h_rec = 440
w_rec = int(iso_rec.width * (h_rec / iso_rec.height))
r_rec = iso_rec.resize((w_rec, h_rec), Image.Resampling.LANCZOS)

# 4. Color / Lighting Harmonization (morning sunlight)
def harmonize_light(img, warm_boost=1.03, contrast=1.04):
    rgb, a = img.convert('RGB'), img.split()[-1]
    rgb = ImageEnhance.Brightness(rgb).enhance(warm_boost)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    res = rgb.convert('RGBA')
    res.putalpha(a)
    return res

r_spr = harmonize_light(r_spr)
r_mik = harmonize_light(r_mik)
r_rec = harmonize_light(r_rec)

# 5. Realistic Shadow Generation
def make_drop_shadow(img, offset_x=12, offset_y=20, blur=16, opacity=0.42):
    a = img.split()[-1]
    shadow_mask = a.point(lambda p: int(p * opacity))
    shadow = Image.new('RGBA', img.size, (20, 16, 12, 255))
    shadow.putalpha(shadow_mask)
    return shadow.filter(ImageFilter.GaussianBlur(blur))

def make_contact_shadow(width, height=16, opacity=0.75, blur=5):
    from PIL import ImageDraw
    s = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.ellipse((0, 0, width, height), fill=(18, 14, 10, int(255 * opacity)))
    return s.filter(ImageFilter.GaussianBlur(blur))

# Position coordinates on the travertine tray
# Tray base is around y=720..830
pos_spr = (110, 480)
pos_mik = (250, 525)
pos_rec = (385, 510)

comp = bg.copy()

# Cast shadows
sh_spr = make_drop_shadow(r_spr, opacity=0.45, blur=18)
sh_mik = make_drop_shadow(r_mik, opacity=0.42, blur=15)
sh_rec = make_drop_shadow(r_rec, opacity=0.40, blur=14)

comp.paste(sh_spr, (pos_spr[0] + 12, pos_spr[1] + 18), sh_spr)
comp.paste(sh_mik, (pos_mik[0] + 10, pos_mik[1] + 16), sh_mik)
comp.paste(sh_rec, (pos_rec[0] + 8, pos_rec[1] + 14), sh_rec)

# Contact base shadows
cs_spr = make_contact_shadow(r_spr.width - 25, height=14, opacity=0.75, blur=5)
cs_mik = make_contact_shadow(r_mik.width - 30, height=14, opacity=0.70, blur=5)
cs_rec = make_contact_shadow(r_rec.width - 20, height=14, opacity=0.70, blur=5)

comp.paste(cs_spr, (pos_spr[0] + 12, pos_spr[1] + r_spr.height - 12), cs_spr)
comp.paste(cs_mik, (pos_mik[0] + 15, pos_mik[1] + r_mik.height - 12), cs_mik)
comp.paste(cs_rec, (pos_rec[0] + 10, pos_rec[1] + r_rec.height - 12), cs_rec)

# Paste official products
comp.paste(r_spr, pos_spr, r_spr)
comp.paste(r_mik, pos_mik, r_mik)
comp.paste(r_rec, pos_rec, r_rec)

# Save final composite
out_comp = 'visuales/set_ritual_exact_composite.jpg'
comp.convert('RGB').save(out_comp, quality=96)
print(f"[OK] Composite saved to {out_comp}")
