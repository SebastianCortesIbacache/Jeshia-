import os
import shutil
import subprocess
import base64
from PIL import Image

# 1. Copy generated image to assets/visuales
artifact_src = r"C:\Users\Wusch\.gemini\antigravity-ide\brain\578ab548-d975-4692-bc32-38b3e2339992\set_ritual_botanico_1786918556655.jpg"
target_photo = r"assets\visuales\set_ritual_botanico_photo.jpg"

if os.path.exists(artifact_src):
    shutil.copy2(artifact_src, target_photo)
    print(f"Copied photo to {target_photo}")

def get_b64(path):
    if not os.path.exists(path):
        return ""
    ext = path.split('.')[-1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/webp'
    with open(path, 'rb') as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')

photo_b64 = get_b64(target_photo)
logo_b64 = get_b64("assets/logos/Jeshia Colores_Transparent.png")
logo_original_b64 = get_b64("assets/logos/Original_Transparent.png")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Montserrat:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;0,800;1,400;1,600&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  
  body {{
    width: 1080px;
    height: 1350px;
    font-family: 'Montserrat', sans-serif;
    position: relative;
    overflow: hidden;
    background-color: #FBF8F3;
    color: #2A2723;
  }}

  /* Full Bleed Visual Photo Container */
  .photo-background {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1080px;
    height: 1350px;
    background-image: url('{photo_b64}');
    background-size: cover;
    background-position: center top;
    z-index: 1;
  }}

  /* Gradient Overlay for Editorial Legibility */
  .gradient-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1080px;
    height: 1350px;
    background: linear-gradient(180deg, 
      rgba(251, 248, 243, 0.96) 0%, 
      rgba(251, 248, 243, 0.85) 18%, 
      rgba(251, 248, 243, 0.15) 38%, 
      rgba(12, 15, 12, 0.20) 65%, 
      rgba(12, 15, 12, 0.92) 88%,
      rgba(12, 15, 12, 0.98) 100%);
    z-index: 2;
  }}

  /* Luxury Border Frame */
  .outer-frame {{
    position: absolute;
    top: 28px;
    left: 28px;
    right: 28px;
    bottom: 28px;
    border: 1.5px solid rgba(196, 122, 71, 0.65);
    pointer-events: none;
    z-index: 20;
  }}

  .inner-frame {{
    position: absolute;
    top: 36px;
    left: 36px;
    right: 36px;
    bottom: 36px;
    border: 1px solid rgba(212, 163, 115, 0.35);
    pointer-events: none;
    z-index: 20;
  }}

  .corner-flower {{
    position: absolute;
    width: 18px;
    height: 18px;
    color: #C47A47;
    z-index: 25;
  }}
  .corner-tl {{ top: 22px; left: 22px; }}
  .corner-tr {{ top: 22px; right: 22px; }}
  .corner-bl {{ bottom: 22px; left: 22px; }}
  .corner-br {{ bottom: 22px; right: 22px; }}

  /* Content Wrapper */
  .content-container {{
    position: relative;
    z-index: 10;
    width: 1080px;
    height: 1350px;
    padding: 60px 65px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  /* Header Section */
  .header-section {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }}

  .brand-badge {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(196, 122, 71, 0.12);
    border: 1px solid rgba(196, 122, 71, 0.4);
    padding: 6px 20px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #C47A47;
    margin-bottom: 14px;
  }}

  .logo-wrap {{
    margin-bottom: 12px;
  }}
  .logo-wrap img {{
    height: 68px;
    width: auto;
    object-fit: contain;
  }}

  .headline-wrap {{
    margin-top: 4px;
  }}

  .main-title {{
    font-family: 'Playfair Display', serif;
    font-size: 3.4rem;
    font-weight: 700;
    color: #2A4031;
    line-height: 1.08;
    letter-spacing: -0.01em;
  }}

  .main-title em {{
    font-style: italic;
    font-family: 'Cormorant Garamond', serif;
    color: #C47A47;
    font-weight: 600;
  }}

  .subtitle-tagline {{
    font-size: 0.98rem;
    font-weight: 400;
    color: #555046;
    letter-spacing: 0.05em;
    margin-top: 8px;
    max-width: 780px;
    line-height: 1.45;
  }}

  /* Floating Tag on Image */
  .center-floating-tag {{
    align-self: flex-start;
    margin-top: 40px;
    margin-left: 20px;
    background: rgba(251, 248, 243, 0.92);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(196, 122, 71, 0.35);
    padding: 12px 22px;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    display: inline-flex;
    align-items: center;
    gap: 14px;
  }}

  .center-floating-tag .icon-box {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #2A4031;
    color: #FBF8F3;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
  }}

  .center-floating-tag .tag-text b {{
    display: block;
    font-size: 0.88rem;
    color: #2A4031;
    font-weight: 700;
    letter-spacing: 0.04em;
  }}
  .center-floating-tag .tag-text span {{
    font-size: 0.76rem;
    color: #C47A47;
    font-weight: 600;
  }}

  /* Footer Card Section */
  .footer-card {{
    background: rgba(12, 15, 12, 0.88);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(212, 163, 115, 0.45);
    border-radius: 20px;
    padding: 30px 40px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.45);
    color: #FBF8F3;
  }}

  .card-top-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(212, 163, 115, 0.25);
    padding-bottom: 18px;
    margin-bottom: 18px;
  }}

  .set-includes-title {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.24em;
    color: #D4A373;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .price-box {{
    text-align: right;
  }}
  .price-label {{
    font-size: 0.70rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #A3B18A;
    font-weight: 600;
  }}
  .price-value {{
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
    margin-top: 2px;
  }}
  .price-value span {{
    font-size: 1.1rem;
    color: #D4A373;
    font-family: 'Montserrat', sans-serif;
    font-weight: 400;
  }}

  /* Inclusions Pills Grid */
  .inclusions-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 22px;
  }}

  .inclusion-item {{
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(212, 163, 115, 0.25);
    border-radius: 12px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .inclusion-item .item-icon {{
    font-size: 1.1rem;
  }}

  .inclusion-item .item-text {{
    font-size: 0.78rem;
    font-weight: 600;
    color: #FBF8F3;
    line-height: 1.25;
  }}
  .inclusion-item .item-text small {{
    display: block;
    font-size: 0.68rem;
    font-weight: 400;
    color: #D4A373;
  }}

  /* CTA Row */
  .cta-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .trust-pills {{
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 0.74rem;
    color: #D4A373;
  }}
  .trust-pills span {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .cta-button {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #C47A47 0%, #A85D2D 100%);
    color: #FFFFFF;
    padding: 14px 30px;
    border-radius: 50px;
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    box-shadow: 0 10px 25px rgba(196, 122, 71, 0.45);
    border: 1px solid rgba(255,255,255,0.2);
  }}

  .cta-button .wa-icon {{
    font-size: 1.1rem;
  }}
</style>
</head>
<body>

  <!-- Background Photo -->
  <div class="photo-background"></div>
  <div class="gradient-overlay"></div>

  <!-- Decorative Frames -->
  <div class="outer-frame"></div>
  <div class="inner-frame"></div>

  <!-- Corner Rosettes -->
  <svg class="corner-flower corner-tl" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="3"/><path d="M12 2C10.5 5 10.5 7 12 8C13.5 7 13.5 5 12 2Z"/><path d="M12 22C10.5 19 10.5 17 12 16C13.5 17 13.5 19 12 22Z"/><path d="M2 12C5 10.5 7 10.5 8 12C7 13.5 5 13.5 2 12Z"/><path d="M22 12C19 10.5 17 10.5 16 12C17 13.5 19 13.5 22 12Z"/></svg>
  <svg class="corner-flower corner-tr" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="3"/><path d="M12 2C10.5 5 10.5 7 12 8C13.5 7 13.5 5 12 2Z"/><path d="M12 22C10.5 19 10.5 17 12 16C13.5 17 13.5 19 12 22Z"/><path d="M2 12C5 10.5 7 10.5 8 12C7 13.5 5 13.5 2 12Z"/><path d="M22 12C19 10.5 17 10.5 16 12C17 13.5 19 13.5 22 12Z"/></svg>
  <svg class="corner-flower corner-bl" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="3"/><path d="M12 2C10.5 5 10.5 7 12 8C13.5 7 13.5 5 12 2Z"/><path d="M12 22C10.5 19 10.5 17 12 16C13.5 17 13.5 19 12 22Z"/><path d="M2 12C5 10.5 7 10.5 8 12C7 13.5 5 13.5 2 12Z"/><path d="M22 12C19 10.5 17 10.5 16 12C17 13.5 19 13.5 22 12Z"/></svg>
  <svg class="corner-flower corner-br" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="3"/><path d="M12 2C10.5 5 10.5 7 12 8C13.5 7 13.5 5 12 2Z"/><path d="M12 22C10.5 19 10.5 17 12 16C13.5 17 13.5 19 12 22Z"/><path d="M2 12C5 10.5 7 10.5 8 12C7 13.5 5 13.5 2 12Z"/><path d="M22 12C19 10.5 17 10.5 16 12C17 13.5 19 13.5 22 12Z"/></svg>

  <!-- Main Layout Content -->
  <div class="content-container">
    
    <!-- Top Header -->
    <div class="header-section">
      <div class="brand-badge">
        <span>✦</span> EDICIÓN ESPECIAL DE REGALO <span>✦</span>
      </div>

      <div class="logo-wrap">
        <img src="{logo_b64}" alt="Jeshia Logo">
      </div>

      <div class="headline-wrap">
        <h1 class="main-title">Set Ritual <em>Botánico</em></h1>
        <p class="subtitle-tagline">
          La experiencia olfativa integral para transformar tu hogar en un santuario de serenidad y sofisticación artesanal.
        </p>
      </div>
    </div>

    <!-- Center Floating Feature Tag -->
    <div class="center-floating-tag">
      <div class="icon-box">🎁</div>
      <div class="tag-text">
        <b>Presentación Premium</b>
        <span>Caja artesanal con lazo de lino botánico</span>
      </div>
    </div>

    <!-- Bottom Footer Card -->
    <div class="footer-card">
      <div class="card-top-row">
        <div>
          <div class="set-includes-title">
            <span>🌿</span> Experiencia Olfativa 3 en 1
          </div>
          <div style="font-size: 0.95rem; font-weight: 600; color: #FBF8F3; margin-top: 4px;">
            Elige tu fragancia favorita o combina notas complementarias
          </div>
        </div>
        <div class="price-box">
          <div class="price-label">Precio Exclusivo</div>
          <div class="price-value">$26.000 <span>CLP</span></div>
        </div>
      </div>

      <!-- Inclusions Grid -->
      <div class="inclusions-grid">
        <div class="inclusion-item">
          <span class="item-icon">🛋️</span>
          <div class="item-text">
            Home Spray
            <small>250 ml Vidrio Ámbar</small>
          </div>
        </div>

        <div class="inclusion-item">
          <span class="item-icon">🌿</span>
          <div class="item-text">
            Difusor Mikado
            <small>50 ml + 6 Varillas</small>
          </div>
        </div>

        <div class="inclusion-item">
          <span class="item-icon">♻️</span>
          <div class="item-text">
            Recarga Eco
            <small>250 ml Refill</small>
          </div>
        </div>

        <div class="inclusion-item">
          <span class="item-icon">🎀</span>
          <div class="item-text">
            Caja de Regalo
            <small>Lazo de Lino Natural</small>
          </div>
        </div>
      </div>

      <!-- CTA and Trust Badges -->
      <div class="cta-row">
        <div class="trust-pills">
          <span>🌿 100% Botánico</span>
          <span>•</span>
          <span>🚚 Envíos a todo Chile</span>
          <span>•</span>
          <span>✨ 13 Aromas Disponibles</span>
        </div>

        <div class="cta-button">
          <span class="wa-icon">💬</span>
          <span>Pedir por WhatsApp</span>
        </div>
      </div>
    </div>

  </div>

</body>
</html>
"""

with open("set_ritual_mkt.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated set_ritual_mkt.html")

# Render via Microsoft Edge Headless into 1080x1350 px
edge_bin = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
html_file = 'set_ritual_mkt.html'
abs_html = os.path.abspath(html_file).replace('\\', '/')

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

print("Rendering Set Ritual Botánico Ad Poster (1080x1350)...")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(primary_out):
    print(f"[OK] Rendered {primary_out} ({os.path.getsize(primary_out)} bytes)")
    # Also save to assets/visuales
    shutil.copy2(primary_out, 'assets/visuales/set_ritual_mkt_4x5.png')
    print("[OK] Saved copy to assets/visuales/set_ritual_mkt_4x5.png")
else:
    print(f"[ERROR] Rendering failed: {res.stderr}")
