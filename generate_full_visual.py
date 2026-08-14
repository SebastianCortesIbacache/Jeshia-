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

# We use v_mikado_4.png (Berries studio photography with warm background)
bg_source_path = 'assets/visuales/Mikado/v_mikado_4.png'
if not os.path.exists(bg_source_path):
    bg_source_path = 'assets/visuales/Mikado/v_mikado_2.png'

src_img = Image.open(bg_source_path).convert('RGB')
sw, sh = src_img.size
tw, th = 1080, 1350

# Ensure scale covers both dimensions fully with NO BLACK BARS
scale = max(tw / sw, th / sh)
nw, nh = int(sw * scale), int(sh * scale)
scaled_img = src_img.resize((nw, nh), Image.Resampling.LANCZOS)

# Position crop to place product bottle nicely on the right half
left = nw - tw
top = nh - th
bg_canvas = scaled_img.crop((left, top, left + tw, top + th))
bg_canvas_path = 'visuales/bg_mikado_poster.jpg'
bg_canvas.save(bg_canvas_path, quality=96)

bg_b64 = get_b64(bg_canvas_path)
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
    color: #422917;
  }}

  /* Full Screen Background Photography */
  .bg-img {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1080px;
    height: 1350px;
    background-image: url('{bg_b64}');
    background-size: cover;
    background-position: right center;
    z-index: 1;
  }}

  /* Studio Lighting Scrim on Left for Clean Legible Typography */
  .bg-scrim {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1080px;
    height: 1350px;
    background: linear-gradient(
      90deg, 
      rgba(247, 241, 233, 0.94) 0%, 
      rgba(247, 241, 233, 0.85) 45%,
      rgba(247, 241, 233, 0.20) 75%,
      rgba(247, 241, 233, 0.0) 100%
    );
    z-index: 2;
  }}

  /* Outer Border Frame with Cross Marker */
  .outer-frame {{
    position: absolute;
    top: 25px;
    left: 25px;
    right: 25px;
    bottom: 25px;
    border: 1.5px solid #634024;
    pointer-events: none;
    z-index: 10;
  }}
  .outer-frame::before {{
    content: "+";
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    color: #634024;
    font-size: 16px;
    font-weight: 500;
  }}

  /* Container */
  .container {{
    position: relative;
    z-index: 5;
    width: 100%;
    height: 100%;
    padding: 60px 65px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  /* Top Left Brand Logo */
  .top-left-brand {{
    width: 440px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }}

  .logo-main {{
    width: 250px;
    height: auto;
    object-fit: contain;
    margin-bottom: 10px;
  }}

  .brand-subtext {{
    font-size: 13px;
    font-weight: 700;
    color: #634024;
    letter-spacing: 4px;
    text-transform: uppercase;
    position: relative;
    padding-top: 10px;
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

  /* Middle Left Content */
  .middle-left-content {{
    width: 440px;
    margin-top: -15px;
  }}

  .product-title {{
    font-family: 'Playfair Display', serif;
    font-size: 72px;
    font-weight: 800;
    color: #523118;
    letter-spacing: 3px;
    line-height: 1;
    text-align: center;
    margin-bottom: 14px;
  }}

  .specs-divider-line {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 6px;
    width: 100%;
  }}
  .specs-divider-line::before, .specs-divider-line::after {{
    content: "";
    height: 1px;
    background: #B17A54;
    flex-grow: 1;
    opacity: 0.6;
  }}
  .vol-text {{
    font-size: 17px;
    font-weight: 700;
    color: #634024;
    letter-spacing: 2px;
  }}

  .aroma-text {{
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 23px;
    color: #634024;
    text-align: center;
    margin-bottom: 35px;
  }}

  /* Features List */
  .features-list {{
    display: flex;
    flex-direction: column;
    gap: 22px;
  }}

  .feat-item {{
    display: flex;
    align-items: center;
    gap: 18px;
  }}

  .feat-circle {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 1.5px solid #634024;
    background: rgba(247, 241, 233, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .feat-circle svg {{
    width: 22px;
    height: 22px;
    fill: #634024;
  }}

  .feat-text {{
    font-size: 19px;
    font-weight: 600;
    color: #2D1D13;
    line-height: 1.25;
  }}

  /* Bottom Left Price Box */
  .bottom-left-section {{
    width: 440px;
  }}

  .price-box {{
    border: 1.5px solid #634024;
    border-radius: 16px;
    background: #B17A54;
    color: #FFFFFF;
    padding: 16px 25px;
    text-align: center;
    box-shadow: 0 8px 22px rgba(99, 64, 36, 0.22);
  }}

  .price-title-row {{
    display: flex;
    align-items: center;
    gap: 15px;
    justify-content: center;
    margin-bottom: 2px;
  }}
  .price-title-row::before, .price-title-row::after {{
    content: "";
    height: 1px;
    width: 45px;
    background: rgba(255, 255, 255, 0.7);
  }}

  .price-title {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-style: italic;
  }}

  .price-amount {{
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: 1px;
    line-height: 1.1;
  }}

  /* Footer Line */
  .footer-bar {{
    position: absolute;
    bottom: 40px;
    left: 65px;
    right: 65px;
    border-top: 1px solid #634024;
    padding-top: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 15px;
    font-weight: 600;
    color: #422917;
  }}

  .footer-item {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .footer-item svg {{
    width: 18px;
    height: 18px;
    fill: #634024;
  }}
</style>
</head>
<body>
  <div class="bg-img"></div>
  <div class="bg-scrim"></div>
  <div class="outer-frame"></div>

  <div class="container">
    <!-- Top Left Brand Logo -->
    <div class="top-left-brand">
      <img src="{logo_black_b64}" class="logo-main" alt="Logo Jeshia">
      <div class="brand-subtext">HOME & AROMAS</div>
    </div>

    <!-- Middle Left Details -->
    <div class="middle-left-content">
      <h1 class="product-title">MIKADO</h1>

      <div class="specs-divider-line">
        <span class="vol-text">50 ML</span>
      </div>
      <div class="aroma-text">Aroma Permanente</div>

      <div class="features-list">
        <div class="feat-item">
          <div class="feat-circle">
            <svg viewBox="0 0 24 24"><path d="M12 3v3M9 4l1.5 2M15 4l-1.5 2M8 10h8v2a4 4 0 01-4 4 4 4 0 01-4-4v-2zM7 20h10v1H7z" stroke="#634024" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>
          </div>
          <span class="feat-text">Aromatiza tu<br>ambiente</span>
        </div>

        <div class="feat-item">
          <div class="feat-circle">
            <svg viewBox="0 0 24 24"><path d="M12 8.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7zM12 2a3.5 3.5 0 00-3.5 3.5c0 1.15.54 2.16 1.37 2.8A3.5 3.5 0 005.5 12c0 1.93 1.57 3.5 3.5 3.5c.34 0 .66-.05.97-.14a3.5 3.5 0 005.06 0c.31.09.63.14.97.14 1.93 0 3.5-1.57 3.5-3.5 0-1.15-.54-2.16-1.37-2.8A3.5 3.5 0 0015.5 5.5 3.5 3.5 0 0012 2z" fill="none" stroke="#634024" stroke-width="1.6"/></svg>
          </div>
          <span class="feat-text">Fragancia<br>perdurable</span>
        </div>

        <div class="feat-item">
          <div class="feat-circle">
            <svg viewBox="0 0 24 24"><path d="M6 3l12 18M12 3v18M18 3L6 21" stroke="#634024" stroke-width="1.8" stroke-linecap="round"/></svg>
          </div>
          <span class="feat-text">13 aromas<br>disponibles</span>
        </div>
      </div>
    </div>

    <!-- Bottom Left Price Box -->
    <div class="bottom-left-section">
      <div class="price-box">
        <div class="price-title-row">
          <span class="price-title">Valor</span>
        </div>
        <div class="price-amount">$10.000</div>
      </div>
    </div>

    <!-- Bottom Footer Bar -->
    <div class="footer-bar">
      <div class="footer-item">
        <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
        <span>WhatsApp: +56 9 3114 1134 / +56 9 3362 0641</span>
      </div>
      <div class="footer-item">
        <span>TikTok: @jeshiacybn</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

with open('mikado_full_visual.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Saved exact editorial poster HTML replicate with v_mikado_4.png background.")
