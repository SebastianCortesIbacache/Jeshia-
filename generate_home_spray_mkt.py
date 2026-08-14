import os
import subprocess
import base64
from PIL import Image

def get_b64(path):
    if not os.path.exists(path):
        return ""
    ext = path.split('.')[-1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/webp'
    with open(path, 'rb') as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')

# 1. Prepare intact product photograph for right column (580 x 1350 px canvas)
# Using v_home_spray_1.png (original size: 768 x 1365 px)
src_path = 'assets/visuales/Home Spray/v_home_spray_1.png'
if not os.path.exists(src_path):
    src_path = 'assets/visuales/Home Spray/v_home_spray_2.png'

src_img = Image.open(src_path).convert('RGB')
sw, sh = src_img.size
target_w, target_h = 580, 1350

# Scale to fit height 1350 px
scale = target_h / sh
nw, nh = int(sw * scale), target_h
scaled = src_img.resize((nw, nh), Image.Resampling.LANCZOS)

# Crop width to 580px centered on the bottle
if nw > target_w:
    left = (nw - target_w) // 2
    crop_right = scaled.crop((left, 0, left + target_w, target_h))
else:
    # If narrower, pad background softly
    crop_right = Image.new('RGB', (target_w, target_h), (248, 244, 238))
    left = (target_w - nw) // 2
    crop_right.paste(scaled, (left, 0))

right_col_path = 'visuales/home_spray_right_col.jpg'
crop_right.save(right_col_path, quality=96)

right_b64 = get_b64(right_col_path)
logo_black_b64 = get_b64('assets/logos/Original_Transparent.png')

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,400;1,600&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1350px;
    font-family: 'Montserrat', sans-serif;
    position: relative;
    overflow: hidden;
    background-color: #F8F4EE;
    color: #422917;
  }}

  /* Outer Double Border Frame with Centered Editorial Markers */
  .outer-frame {{
    position: absolute;
    top: 25px;
    left: 25px;
    right: 25px;
    bottom: 25px;
    border: 1.5px solid #634024;
    pointer-events: none;
    z-index: 30;
  }}
  .inner-frame {{
    position: absolute;
    top: 31px;
    left: 31px;
    right: 31px;
    bottom: 31px;
    border: 1px solid rgba(177, 122, 84, 0.35);
    pointer-events: none;
    z-index: 30;
  }}
  .outer-frame::before {{
    content: "+";
    position: absolute;
    top: -13px;
    left: 50%;
    transform: translateX(-50%);
    color: #634024;
    font-size: 16px;
    font-weight: 500;
  }}
  .outer-frame::after {{
    content: "•";
    position: absolute;
    bottom: -11px;
    left: 50%;
    transform: translateX(-50%);
    color: #634024;
    font-size: 14px;
  }}

  /* Split 2-Column Canvas */
  .canvas {{
    display: flex;
    width: 1080px;
    height: 1350px;
    position: relative;
    z-index: 5;
  }}

  /* Left Column (500px): Typography & Branding */
  .col-left {{
    width: 500px;
    height: 1350px;
    padding: 60px 45px 50px 55px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: #F8F4EE;
    z-index: 10;
  }}

  /* Right Column (580px): Unmodified Product Photography */
  .col-right {{
    width: 580px;
    height: 1350px;
    position: relative;
    overflow: hidden;
    z-index: 5;
  }}

  .product-img {{
    width: 580px;
    height: 1350px;
    object-fit: cover;
  }}

  /* Header Section */
  .header-group {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }}

  .logo-img {{
    width: 240px;
    height: auto;
    object-fit: contain;
    margin-bottom: 8px;
  }}

  .brand-subtext {{
    font-size: 12px;
    font-weight: 700;
    color: #634024;
    letter-spacing: 4px;
    text-transform: uppercase;
    position: relative;
    padding-top: 8px;
    width: 100%;
  }}
  .brand-subtext::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 15%;
    right: 15%;
    height: 1px;
    background: #B17A54;
    opacity: 0.6;
  }}

  /* Main Title & Format */
  .title-group {{
    text-align: center;
    margin-top: -10px;
  }}

  .main-title {{
    font-family: 'Playfair Display', serif;
    font-size: 58px;
    font-weight: 800;
    color: #523118;
    letter-spacing: 2px;
    line-height: 1.05;
    margin-bottom: 12px;
  }}

  .vol-line {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 6px;
  }}
  .vol-line::before, .vol-line::after {{
    content: "";
    height: 1px;
    background: #B17A54;
    flex-grow: 1;
    opacity: 0.5;
  }}
  .vol-text {{
    font-size: 16px;
    font-weight: 700;
    color: #634024;
    letter-spacing: 2px;
  }}

  .bajada-text {{
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 21px;
    color: #634024;
    margin-top: 4px;
  }}

  /* Three Linear Icons & Characteristics */
  .features-group {{
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 10px;
  }}

  .feat-item {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .feat-circle {{
    width: 46px;
    height: 46px;
    border-radius: 50%;
    border: 1.5px solid #634024;
    background: #F8F4EE;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .feat-circle svg {{
    width: 22px;
    height: 22px;
    stroke: #634024;
    fill: none;
    stroke-width: 1.6;
    stroke-linecap: round;
    stroke-linejoin: round;
  }}

  .feat-label {{
    font-size: 17px;
    font-weight: 600;
    color: #2D1D13;
    line-height: 1.25;
  }}

  /* Price Card */
  .price-box {{
    border: 1.5px solid #634024;
    border-radius: 16px;
    background: #B17A54;
    color: #FFFFFF;
    padding: 16px 20px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(99, 64, 36, 0.2);
    margin-top: 10px;
  }}

  .price-title-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    justify-content: center;
    margin-bottom: 2px;
  }}
  .price-title-row::before, .price-title-row::after {{
    content: "";
    height: 1px;
    width: 40px;
    background: rgba(255, 255, 255, 0.7);
  }}

  .price-title {{
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-style: italic;
  }}

  .price-val {{
    font-family: 'Playfair Display', serif;
    font-size: 50px;
    font-weight: 700;
    letter-spacing: 1px;
    line-height: 1.05;
  }}

  /* Discreet Contact Footer */
  .contact-footer {{
    border-top: 1px solid #634024;
    padding-top: 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 13.5px;
    font-weight: 600;
    color: #554030;
    width: 100%;
  }}

  .contact-row {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .contact-row svg {{
    width: 15px;
    height: 15px;
    fill: #634024;
  }}
</style>
</head>
<body>
  <div class="outer-frame"></div>
  <div class="inner-frame"></div>

  <div class="canvas">
    <!-- Left Column: Branding, Text & Details -->
    <div class="col-left">
      <!-- Header -->
      <div class="header-group">
        <img src="{logo_black_b64}" class="logo-img" alt="Logo Jeshia">
        <div class="brand-subtext">HOME & AROMAS</div>
      </div>

      <!-- Main Title -->
      <div class="title-group">
        <h1 class="main-title">Home Spray</h1>
        <div class="vol-line">
          <span class="vol-text">250 ML</span>
        </div>
        <div class="bajada-text">Aromas para cuando lo desees</div>
      </div>

      <!-- 3 Features -->
      <div class="features-group">
        <div class="feat-item">
          <div class="feat-circle">
            <svg viewBox="0 0 24 24"><path d="M12 3v3M9 4l1.5 2M15 4l-1.5 2M8 10h8v2a4 4 0 01-4 4 4 4 0 01-4-4v-2zM7 20h10v1H7z"/></svg>
          </div>
          <span class="feat-label">Aromatiza al Momento</span>
        </div>

        <div class="feat-item">
          <div class="feat-circle">
            <svg viewBox="0 0 24 24"><path d="M12 8.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7zM12 2a3.5 3.5 0 00-3.5 3.5c0 1.15.54 2.16 1.37 2.8A3.5 3.5 0 005.5 12c0 1.93 1.57 3.5 3.5 3.5c.34 0 .66-.05.97-.14a3.5 3.5 0 005.06 0c.31.09.63.14.97.14 1.93 0 3.5-1.57 3.5-3.5 0-1.15-.54-2.16-1.37-2.8A3.5 3.5 0 0015.5 5.5 3.5 3.5 0 0012 2z"/></svg>
          </div>
          <span class="feat-label">Fragancia que perdura</span>
        </div>

        <div class="feat-item">
          <div class="feat-circle">
            <svg viewBox="0 0 24 24"><path d="M6 3l12 18M12 3v18M18 3L6 21"/></svg>
          </div>
          <span class="feat-label">13 aromas</span>
        </div>
      </div>

      <!-- Price -->
      <div class="price-box">
        <div class="price-title-row">
          <span class="price-title">Valor</span>
        </div>
        <div class="price-val">$12.000</div>
      </div>

      <!-- Contact -->
      <div class="contact-footer">
        <div class="contact-row">
          <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <span>WhatsApp: +56 9 3114 1134 / +56 9 3362 0641</span>
        </div>
        <div class="contact-row">
          <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
          <span>TikTok: @jeshiacybn</span>
        </div>
      </div>
    </div>

    <!-- Right Column: Unmodified Product Photo -->
    <div class="col-right">
      <img src="{right_b64}" class="product-img" alt="Home Spray Mokka Jeshia">
    </div>
  </div>
</body>
</html>
"""

with open('home_spray_mkt.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Saved updated home_spray_mkt.html script successfully.")
