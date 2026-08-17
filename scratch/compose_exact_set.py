import os
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np

# Load background scene (with the gift box, travertine tray, table, sofa)
bg_path = 'assets/visuales/set_ritual_botanico_photo.jpg'
bg = Image.open(bg_path).convert('RGBA')
bg_w, bg_h = bg.size  # (896, 1200)

# Load official product photos
p_spray = 'assets/montajes/oficiales/Home Spray Sin Marca.png'
p_mikado = 'assets/montajes/oficiales/Mikado Sin Marca.png'
p_recarga = 'assets/montajes/oficiales/Recarga 250 Sin Marca 2.png'

im_spray = Image.open(p_spray).convert('RGB')
im_mikado = Image.open(p_mikado).convert('RGB')
im_recarga = Image.open(p_recarga).convert('RGB')

def isolate_product(img, bg_color_sample=(250, 240, 230), tol=18, feather=2):
    # Convert to array
    arr = np.array(img).astype(np.float32)
    
    # Sample background color from borders
    top_left = arr[10:50, 10:50].mean(axis=(0,1))
    top_right = arr[10:50, -50:-10].mean(axis=(0,1))
    bg_col = (top_left + top_right) / 2.0
    
    # Distance from background
    diff = np.sqrt(np.sum((arr - bg_col)**2, axis=2))
    
    # Soft alpha mask
    mask = np.clip((diff - tol) / (tol * 1.5), 0, 1)
    mask = (mask * 255).astype(np.uint8)
    
    mask_img = Image.fromarray(mask, mode='L')
    if feather > 0:
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(feather))
        
    rgba = img.convert('RGBA')
    rgba.putalpha(mask_img)
    return rgba

print("Isolating official products...")
# Let's crop tight before isolating
crop_mik = im_mikado.crop((780, 80, 1620, 1500))
crop_spr = im_spray.crop((820, 40, 1580, 1560))
crop_rec = im_recarga.crop((880, 60, 1520, 1540))

iso_mik = isolate_product(crop_mik, tol=15, feather=1.5)
iso_spr = isolate_product(crop_spr, tol=15, feather=1.5)
iso_rec = isolate_product(crop_rec, tol=15, feather=1.5)

# Now, let's prepare the background:
# We want to cover/clean the old AI bottles in bg
# In bg (896, 1200):
# The old AI bottles are located roughly from x=50 to x=480, y=500 to y=980
# The clean table is below, and clean sofa is above.
# Let's clone/paint clean table and sofa background over the old AI bottles
clean_bg = bg.copy()

# Composite the 3 official isolated products onto the clean background in front of the gift box:
# Set Ritual scale on (896, 1200) canvas:
# 1. Home Spray (left, standing tall ~460px high)
h_spray = 480
w_spray = int(iso_spr.width * (h_spray / iso_spr.height))
r_spr = iso_spr.resize((w_spray, h_spray), Image.Resampling.LANCZOS)

# 2. Mikado (center-left, ~420px high)
h_mik = 430
w_mik = int(iso_mik.width * (h_mik / iso_mik.height))
r_mik = iso_mik.resize((w_mik, h_mik), Image.Resampling.LANCZOS)

# 3. Recarga Eco (between Mikado and Box, ~400px high)
h_rec = 410
w_rec = int(iso_rec.width * (h_rec / iso_rec.height))
r_rec = iso_rec.resize((w_rec, h_rec), Image.Resampling.LANCZOS)

# Create composite scene
comp = bg.copy()

# Add soft drop shadows for each bottle
def create_shadow(img, offset_x=10, offset_y=18, blur=15, opacity=0.45):
    alpha = img.split()[-1]
    shadow_mask = alpha.point(lambda p: int(p * opacity))
    shadow = Image.new('RGBA', img.size, (15, 12, 10, 255))
    shadow.putalpha(shadow_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow

sh_spr = create_shadow(r_spr, offset_x=15, offset_y=25, blur=18, opacity=0.55)
sh_mik = create_shadow(r_mik, offset_x=12, offset_y=20, blur=15, opacity=0.50)
sh_rec = create_shadow(r_rec, offset_x=10, offset_y=18, blur=14, opacity=0.45)

# Positions on table / tray in front of gift box
# Gift box is around x=440..780, y=430..800
pos_spr = (70, 520)
pos_mik = (210, 570)
pos_rec = (360, 590)

# Paste shadows
comp.paste(sh_spr, (pos_spr[0] + 12, pos_spr[1] + 20), sh_spr)
comp.paste(sh_mik, (pos_mik[0] + 10, pos_mik[1] + 16), sh_mik)
comp.paste(sh_rec, (pos_rec[0] + 8, pos_rec[1] + 14), sh_rec)

# Paste products
comp.paste(r_spr, pos_spr, r_spr)
comp.paste(r_mik, pos_mik, r_mik)
comp.paste(r_rec, pos_rec, r_rec)

out_comp = 'visuales/set_ritual_exact_composite.jpg'
comp.convert('RGB').save(out_comp, quality=95)
print(f"Composite saved to {out_comp}")
