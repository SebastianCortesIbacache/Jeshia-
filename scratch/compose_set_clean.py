import os
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np

# 1. Clean background image path
bg_path = r"C:\Users\Wusch\.gemini\antigravity-ide\brain\578ab548-d975-4692-bc32-38b3e2339992\clean_set_ritual_box_1786923237084.jpg"
bg = Image.open(bg_path).convert('RGBA')
bw, bh = bg.size  # 896 x 1200

# 2. Official products from E:\Logo Jeshia\assets\montajes\oficiales
p_spray = 'assets/montajes/oficiales/Home Spray Sin Marca.png'
p_mikado = 'assets/montajes/oficiales/Mikado Sin Marca.png'
p_recarga = 'assets/montajes/oficiales/Recarga 250 Sin Marca 2.png'

im_spray = Image.open(p_spray).convert('RGB')
im_mikado = Image.open(p_mikado).convert('RGB')
im_recarga = Image.open(p_recarga).convert('RGB')

# High quality alpha extraction from studio solid background
def extract_bottle(img, box, threshold=22, feather_radius=1.5):
    cropped = img.crop(box)
    arr = np.array(cropped).astype(np.float32)
    
    # Sample background color from outer borders
    corners = np.vstack([
        arr[0:25, 0:25].reshape(-1, 3),
        arr[0:25, -25:].reshape(-1, 3)
    ])
    bg_color = corners.mean(axis=0)
    
    diff = np.sqrt(np.sum((arr - bg_color)**2, axis=2))
    
    # Ramp alpha transition
    alpha = np.clip((diff - threshold) / (threshold * 0.8), 0, 1)
    alpha = (alpha * 255).astype(np.uint8)
    
    alpha_img = Image.fromarray(alpha, mode='L')
    if feather_radius > 0:
        alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(feather_radius))
        
    rgba = cropped.convert('RGBA')
    rgba.putalpha(alpha_img)
    return rgba

print("Extracting official bottles...")
# Bounding box crops
# Spray: trigger top (y~60), bottle bottom (y~1550), width (x~840..1560)
iso_spray = extract_bottle(im_spray, (830, 40, 1570, 1560), threshold=18, feather_radius=1.2)

# Mikado: sticks top (y~80), glass bottom (y~1480), width (x~770..1630)
iso_mikado = extract_bottle(im_mikado, (760, 70, 1640, 1490), threshold=16, feather_radius=1.2)

# Recarga 250: cap top (y~70), bottle bottom (y~1530), width (x~890..1510)
iso_recarga = extract_bottle(im_recarga, (880, 50, 1520, 1540), threshold=16, feather_radius=1.2)

# 3. Scale bottles to match realistic physical proportions on the travertine tray:
# Travertine tray surface is roughly at y=680..850, x=100..750
# Tray height perspective: Box is 200px tall.
# Home Spray should be ~ 430px tall
h_spray = 420
w_spray = int(iso_spray.width * (h_spray / iso_spray.height))
r_spray = iso_spray.resize((w_spray, h_spray), Image.Resampling.LANCZOS)

# Mikado (glass is compact ~180px, with sticks total ~ 370px)
h_mik = 370
w_mik = int(iso_mikado.width * (h_mik / iso_mikado.height))
r_mik = iso_mikado.resize((w_mik, h_mik), Image.Resampling.LANCZOS)

# Recarga 250 (height ~ 390px)
h_rec = 380
w_rec = int(iso_recarga.width * (h_rec / iso_recarga.height))
r_rec = iso_recarga.resize((w_rec, h_rec), Image.Resampling.LANCZOS)

# Color & Warmth Harmonization: slight warm tint to match the sunny morning room
def warm_tint(rgba_img, brightness=1.02, contrast=1.04):
    rgb, a = rgba_img.convert('RGB'), rgba_img.split()[-1]
    rgb = ImageEnhance.Brightness(rgb).enhance(brightness)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    res = rgb.convert('RGBA')
    res.putalpha(a)
    return res

r_spray = warm_tint(r_spray)
r_mik = warm_tint(r_mik)
r_rec = warm_tint(r_rec)

# Realistic Contact & Directional Cast Shadows on the Travertine Stone
def create_realistic_shadow(img, angle_x=8, angle_y=16, blur=14, opacity=0.48):
    a = img.split()[-1]
    # Shadow mask
    s_mask = a.point(lambda p: int(p * opacity))
    shadow = Image.new('RGBA', img.size, (25, 20, 15, 255))
    shadow.putalpha(s_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow

def create_contact_shadow(width, height=18, opacity=0.75, blur=6):
    s = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    # Draw oval contact
    from PIL import ImageDraw
    d = ImageDraw.Draw(s)
    d.ellipse((0, 0, width, height), fill=(20, 15, 12, int(255 * opacity)))
    return s.filter(ImageFilter.GaussianBlur(blur))

# Placements on the travertine tray:
# Box is on the right (x=480..850, y=520..760)
# Tray interior space is (x=120..520, y=600..790)

# Position 1: Home Spray (standing left on tray/table)
pos_spray = (130, 480)
# Position 2: Mikado (center on tray)
pos_mikado = (260, 520)
# Position 3: Recarga Eco 250 (next to box)
pos_recarga = (390, 500)

final_comp = bg.copy()

# 1. Cast shadows
sh_spray = create_realistic_shadow(r_spray, opacity=0.45, blur=16)
sh_mik = create_realistic_shadow(r_mik, opacity=0.42, blur=14)
sh_rec = create_realistic_shadow(r_rec, opacity=0.40, blur=12)

final_comp.paste(sh_spray, (pos_spray[0] - 8, pos_spray[1] + 18), sh_spray)
final_comp.paste(sh_mik, (pos_mikado[0] - 6, pos_mikado[1] + 16), sh_mik)
final_comp.paste(sh_rec, (pos_recarga[0] - 5, pos_recarga[1] + 14), sh_rec)

# 2. Contact base shadows
cs_spray = create_contact_shadow(r_spray.width - 20, height=14, opacity=0.70, blur=5)
cs_mik = create_contact_shadow(r_mik.width - 20, height=14, opacity=0.65, blur=5)
cs_rec = create_contact_shadow(r_rec.width - 20, height=14, opacity=0.65, blur=5)

final_comp.paste(cs_spray, (pos_spray[0] + 10, pos_spray[1] + r_spray.height - 12), cs_spray)
final_comp.paste(cs_mik, (pos_mikado[0] + 10, pos_mikado[1] + r_mik.height - 12), cs_mik)
final_comp.paste(cs_rec, (pos_recarga[0] + 10, pos_recarga[1] + r_rec.height - 12), cs_rec)

# 3. Paste actual products
final_comp.paste(r_spray, pos_spray, r_spray)
final_comp.paste(r_mik, pos_mikado, r_mik)
final_comp.paste(r_rec, pos_recarga, r_rec)

# Save result
out_composite = 'visuales/set_ritual_botanico_lifestyle_oficial.jpg'
final_comp.convert('RGB').save(out_composite, quality=96)
print(f"[OK] Perfect composite saved to {out_composite}")
