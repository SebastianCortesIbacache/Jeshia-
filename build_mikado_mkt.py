import os
import subprocess
import base64

def get_b64(path):
    if not os.path.exists(path):
        return ""
    ext = path.split('.')[-1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/webp'
    with open(path, 'rb') as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')

# Load Base64 assets
logo_b64 = get_b64('assets/logos/Jeshia Colores_Transparent.png')
if not logo_b64:
    logo_b64 = get_b64('assets/logos/Original_Transparent.png')

prod1_b64 = get_b64('visuales/Mikado - Berries Visual.png')
prod2_b64 = get_b64('assets/visuales/Mikado/v_mikado_1.png')
prod3_b64 = get_b64('assets/visuales/Mikado/v_mikado_2.png')

# HTML Template 1: Instagram Post Portrait (1080 x 1350 px - 4:5)
html_1 = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1350px;
    background: #F9F5F0;
    font-family: 'Montserrat', sans-serif;
    color: #000000;
    display: flex;
    overflow: hidden;
    position: relative;
  }}

  /* Background Ambient Effects */
  .bg-decor {{
    position: absolute;
    top: -100px;
    right: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(212, 196, 181, 0.35) 0%, rgba(249, 245, 240, 0) 70%);
    border-radius: 50%;
    z-index: 1;
  }}

  /* Left Side: Product Display */
  .left-container {{
    width: 48%;
    height: 100%;
    position: relative;
    z-index: 2;
    padding: 40px 0 40px 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}

  .product-frame {{
    width: 100%;
    height: 90%;
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(99, 64, 36, 0.12);
    border: 3px solid #D4C4B5;
    position: relative;
    background: #EFE6DD;
  }}

  .product-frame img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  /* Right Side: Marketing Card */
  .right-container {{
    width: 52%;
    height: 100%;
    padding: 50px 45px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 2;
  }}

  .brand-header {{
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
  }}

  .brand-logo {{
    height: 75px;
    object-fit: contain;
  }}

  .brand-subtitle {{
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2.5px;
    color: #634024;
    text-transform: uppercase;
  }}

  .title-section {{
    margin-bottom: 15px;
  }}

  .title-row {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .main-title {{
    font-family: 'Playfair Display', serif;
    font-size: 58px;
    font-weight: 700;
    color: #634024;
    letter-spacing: 1px;
    line-height: 1;
  }}

  .badge-volume {{
    background: #B17A54;
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600;
    padding: 6px 20px;
    border-radius: 50px;
    box-shadow: 0 4px 10px rgba(177, 122, 84, 0.3);
  }}

  .subtitle-text {{
    font-size: 20px;
    font-weight: 600;
    color: #B17A54;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 10px;
  }}

  .divider {{
    display: flex;
    align-items: center;
    margin: 20px 0;
    gap: 15px;
  }}

  .line {{
    flex: 1;
    height: 1px;
    background: #D4C4B5;
  }}

  .leaf-icon {{
    color: #B17A54;
    font-size: 16px;
  }}

  /* Features List */
  .features-list {{
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 25px;
  }}

  .feature-item {{
    display: flex;
    align-items: center;
    gap: 18px;
  }}

  .icon-circle {{
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: #B17A54;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(177, 122, 84, 0.25);
  }}

  .icon-circle svg {{
    width: 26px;
    height: 26px;
    fill: #FFFFFF;
  }}

  .feature-text {{
    font-size: 20px;
    font-weight: 500;
    color: #222222;
    line-height: 1.3;
  }}

  /* Price Card */
  .price-card {{
    background: linear-gradient(135deg, #B17A54 0%, #98633F 100%);
    border-radius: 24px;
    padding: 22px 30px;
    text-align: center;
    color: #FFFFFF;
    box-shadow: 0 10px 25px rgba(177, 122, 84, 0.35);
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
  }}

  .price-card::before {{
    content: '';
    position: absolute;
    top: -20px;
    left: -20px;
    width: 80px;
    height: 80px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
  }}

  .price-label {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-style: italic;
    letter-spacing: 1px;
    opacity: 0.95;
    margin-bottom: 4px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    padding-bottom: 4px;
    display: inline-block;
  }}

  .price-value {{
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: 1px;
  }}

  /* Footer Contact */
  .contact-footer {{
    background: #EFE6DD;
    border-radius: 16px;
    padding: 16px 20px;
    border: 1px solid #D4C4B5;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .contact-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 600;
    color: #634024;
  }}

  .contact-row svg {{
    width: 18px;
    height: 18px;
    fill: #B17A54;
    flex-shrink: 0;
  }}
</style>
</head>
<body>
  <div class="bg-decor"></div>
  
  <!-- Left Side Product Image -->
  <div class="left-container">
    <div class="product-frame">
      <img src="{prod1_b64}" alt="Mikado Jeshia">
    </div>
  </div>

  <!-- Right Side Content -->
  <div class="right-container">
    <div>
      <div class="brand-header">
        <img src="{logo_b64}" class="brand-logo" alt="Logo Jeshia">
      </div>

      <div class="title-section">
        <div class="title-row">
          <h1 class="main-title">MIKADO</h1>
          <span class="badge-volume">50 ml</span>
        </div>
        <div class="subtitle-text">Aroma Permanente</div>
      </div>

      <div class="divider">
        <div class="line"></div>
        <div class="leaf-icon">🌿</div>
        <div class="line"></div>
      </div>

      <div class="features-list">
        <div class="feature-item">
          <div class="icon-circle">
            <!-- Home Mist Icon -->
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
          </div>
          <div class="feature-text">Aromatiza tu ambiente</div>
        </div>

        <div class="feature-item">
          <div class="icon-circle">
            <!-- Wind / Duration Icon -->
            <svg viewBox="0 0 24 24"><path d="M12.5 8c-2.65 0-4.8 2.15-4.8 4.8s2.15 4.8 4.8 4.8 4.8-2.15 4.8-4.8-2.15-4.8-4.8-4.8zm0 8c-1.77 0-3.2-1.43-3.2-3.2s1.43-3.2 3.2-3.2 3.2 1.43 3.2 3.2-1.43 3.2-3.2 3.2zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>
          </div>
          <div class="feature-text">Fragancia perdurable</div>
        </div>

        <div class="feature-item">
          <div class="icon-circle">
            <!-- Aromas / Flowers Icon -->
            <svg viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.2 19.58 10.55 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>
          </div>
          <div class="feature-text">13 aromas disponibles</div>
        </div>
      </div>
    </div>

    <div>
      <div class="price-card">
        <div class="price-label">Valor</div>
        <div class="price-value">$10.000</div>
      </div>

      <div class="contact-footer">
        <div class="contact-row">
          <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <span>WhatsApp: +56 9 3114 1134 / +56 9 3362 0641</span>
        </div>
        <div class="contact-row">
          <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
          <span>TikTok & IG: @jeshiacybn | @jeshia.cl</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# HTML Template 2: Instagram Square Post (1080 x 1080 px - 1:1)
html_2 = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1080px;
    background: #F9F5F0;
    font-family: 'Montserrat', sans-serif;
    color: #000000;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
    padding: 40px;
  }}

  .header-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 2;
  }}

  .logo-img {{
    height: 70px;
    object-fit: contain;
  }}

  .tagline-badge {{
    background: #EFE6DD;
    border: 1px solid #D4C4B5;
    color: #634024;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 1.5px;
    padding: 8px 18px;
    border-radius: 30px;
    text-transform: uppercase;
  }}

  .main-content {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex: 1;
    margin: 20px 0;
    z-index: 2;
  }}

  .info-col {{
    width: 52%;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }}

  .title-group {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .title-row {{
    display: flex;
    align-items: center;
    gap: 15px;
  }}

  .product-name {{
    font-family: 'Playfair Display', serif;
    font-size: 54px;
    font-weight: 700;
    color: #634024;
    line-height: 1;
  }}

  .vol-tag {{
    background: #B17A54;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
    padding: 5px 16px;
    border-radius: 20px;
  }}

  .sub-tag {{
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #B17A54;
    text-transform: uppercase;
  }}

  .feat-container {{
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin: 10px 0;
  }}

  .feat-row {{
    display: flex;
    align-items: center;
    gap: 14px;
    background: #FFFFFF;
    padding: 10px 16px;
    border-radius: 16px;
    border: 1px solid #D4C4B5;
    box-shadow: 0 4px 12px rgba(99, 64, 36, 0.05);
  }}

  .feat-icon {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #B17A54;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .feat-icon svg {{
    width: 20px;
    height: 20px;
    fill: #FFFFFF;
  }}

  .feat-txt {{
    font-size: 17px;
    font-weight: 600;
    color: #222222;
  }}

  .price-box-sq {{
    background: linear-gradient(135deg, #B17A54 0%, #634024 100%);
    color: #FFFFFF;
    padding: 16px 25px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 20px rgba(177, 122, 84, 0.3);
  }}

  .price-lbl {{
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-style: italic;
  }}

  .price-val {{
    font-family: 'Playfair Display', serif;
    font-size: 44px;
    font-weight: 700;
  }}

  .product-col {{
    width: 44%;
    height: 100%;
    max-height: 600px;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(99, 64, 36, 0.15);
    border: 3px solid #D4C4B5;
    background: #EFE6DD;
  }}

  .product-col img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .footer-strip {{
    background: #EFE6DD;
    border-radius: 14px;
    padding: 12px 20px;
    border: 1px solid #D4C4B5;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    font-weight: 600;
    color: #634024;
    z-index: 2;
  }}
</style>
</head>
<body>
  <div class="header-bar">
    <img src="{logo_b64}" class="logo-img" alt="Jeshia Logo">
    <div class="tagline-badge">Belleza & Cosmética Natural</div>
  </div>

  <div class="main-content">
    <div class="info-col">
      <div class="title-group">
        <div class="title-row">
          <h1 class="product-name">MIKADO</h1>
          <span class="vol-tag">50 ml</span>
        </div>
        <div class="sub-tag">Aroma Permanente</div>
      </div>

      <div class="feat-container">
        <div class="feat-row">
          <div class="feat-icon">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
          </div>
          <span class="feat-txt">Aromatiza tu ambiente</span>
        </div>
        <div class="feat-row">
          <div class="feat-icon">
            <svg viewBox="0 0 24 24"><path d="M12.5 8c-2.65 0-4.8 2.15-4.8 4.8s2.15 4.8 4.8 4.8 4.8-2.15 4.8-4.8-2.15-4.8-4.8-4.8zm0 8c-1.77 0-3.2-1.43-3.2-3.2s1.43-3.2 3.2-3.2 3.2 1.43 3.2 3.2-1.43 3.2-3.2 3.2zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>
          </div>
          <span class="feat-txt">Fragancia perdurable</span>
        </div>
        <div class="feat-row">
          <div class="feat-icon">
            <svg viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.2 19.58 10.55 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>
          </div>
          <span class="feat-txt">13 aromas disponibles</span>
        </div>
      </div>

      <div class="price-box-sq">
        <span class="price-lbl">Valor Especial</span>
        <span class="price-val">$10.000</span>
      </div>
    </div>

    <div class="product-col">
      <img src="{prod2_b64 if prod2_b64 else prod1_b64}" alt="Mikado Image">
    </div>
  </div>

  <div class="footer-strip">
    <span>📞 WhatsApp: +56 9 3114 1134 / +56 9 3362 0641</span>
    <span>📱 @jeshiacybn | @jeshia.cl</span>
  </div>
</body>
</html>
"""

# HTML Template 3: Instagram Story / Reel (1080 x 1920 px - 9:16)
html_3 = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1920px;
    background: radial-gradient(circle at center, #F9F5F0 0%, #EFE6DD 100%);
    font-family: 'Montserrat', sans-serif;
    color: #000000;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    overflow: hidden;
    padding: 80px 60px 60px 60px;
  }}

  .header-story {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    text-align: center;
  }}

  .logo-story {{
    height: 95px;
    object-fit: contain;
  }}

  .brand-tag {{
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 3px;
    color: #634024;
    text-transform: uppercase;
  }}

  /* Arch Frame for Product */
  .arch-container {{
    width: 100%;
    height: 720px;
    border-radius: 360px 360px 35px 35px;
    overflow: hidden;
    box-shadow: 0 25px 50px rgba(99, 64, 36, 0.18);
    border: 4px solid #D4C4B5;
    background: #FFFFFF;
    margin: 20px 0;
  }}

  .arch-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  /* Content Card */
  .story-card {{
    width: 100%;
    background: #FFFFFF;
    border-radius: 30px;
    padding: 40px;
    border: 2px solid #D4C4B5;
    box-shadow: 0 15px 40px rgba(99, 64, 36, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 20px;
  }}

  .title-row-story {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
  }}

  .title-story {{
    font-family: 'Playfair Display', serif;
    font-size: 64px;
    font-weight: 700;
    color: #634024;
    line-height: 1;
  }}

  .vol-badge-story {{
    background: #B17A54;
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 600;
    padding: 6px 22px;
    border-radius: 30px;
  }}

  .sub-story {{
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 3px;
    color: #B17A54;
    text-transform: uppercase;
  }}

  .feats-grid {{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin: 10px 0;
  }}

  .feat-card-story {{
    display: flex;
    align-items: center;
    gap: 18px;
    background: #F9F5F0;
    padding: 14px 22px;
    border-radius: 20px;
    border: 1px solid #D4C4B5;
    text-align: left;
  }}

  .feat-icon-story {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #B17A54;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .feat-icon-story svg {{
    width: 24px;
    height: 24px;
    fill: #FFFFFF;
  }}

  .feat-txt-story {{
    font-size: 20px;
    font-weight: 600;
    color: #222222;
  }}

  .price-banner-story {{
    width: 100%;
    background: linear-gradient(135deg, #B17A54 0%, #634024 100%);
    color: #FFFFFF;
    padding: 20px;
    border-radius: 24px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    box-shadow: 0 10px 25px rgba(177, 122, 84, 0.3);
  }}

  .price-lbl-story {{
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-style: italic;
  }}

  .price-val-story {{
    font-family: 'Playfair Display', serif;
    font-size: 56px;
    font-weight: 700;
  }}

  /* Footer Story */
  .footer-story {{
    width: 100%;
    background: #EFE6DD;
    border-radius: 20px;
    padding: 18px 25px;
    border: 1px solid #D4C4B5;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #634024;
  }}
</style>
</head>
<body>
  <div class="header-story">
    <img src="{logo_b64}" class="logo-story" alt="Jeshia Logo">
    <div class="brand-tag">Cosmética & Belleza Natural</div>
  </div>

  <div class="arch-container">
    <img src="{prod3_b64 if prod3_b64 else prod1_b64}" alt="Mikado Story Visual">
  </div>

  <div class="story-card">
    <div>
      <div class="title-row-story">
        <h1 class="title-story">MIKADO</h1>
        <span class="vol-badge-story">50 ml</span>
      </div>
      <div class="sub-story">Aroma Permanente</div>
    </div>

    <div class="feats-grid">
      <div class="feat-card-story">
        <div class="feat-icon-story">
          <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        </div>
        <span class="feat-txt-story">Aromatiza tu ambiente</span>
      </div>
      <div class="feat-card-story">
        <div class="feat-icon-story">
          <svg viewBox="0 0 24 24"><path d="M12.5 8c-2.65 0-4.8 2.15-4.8 4.8s2.15 4.8 4.8 4.8 4.8-2.15 4.8-4.8-2.15-4.8-4.8-4.8zm0 8c-1.77 0-3.2-1.43-3.2-3.2s1.43-3.2 3.2-3.2 3.2 1.43 3.2 3.2-1.43 3.2-3.2 3.2zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>
        </div>
        <span class="feat-txt-story">Fragancia perdurable</span>
      </div>
      <div class="feat-card-story">
        <div class="feat-icon-story">
          <svg viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.2 19.58 10.55 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>
        </div>
        <span class="feat-txt-story">13 aromas disponibles</span>
      </div>
    </div>

    <div class="price-banner-story">
      <span class="price-lbl-story">Valor</span>
      <span class="price-val-story">$10.000</span>
    </div>
  </div>

  <div class="footer-story">
    <div>📱 WhatsApp: +56 9 3114 1134 / +56 9 3362 0641</div>
    <div>✨ TikTok & Instagram: @jeshiacybn | @jeshia.cl</div>
  </div>
</body>
</html>
"""

# Save HTML files
with open('mikado_mkt_1.html', 'w', encoding='utf-8') as f:
    f.write(html_1)

with open('mikado_mkt_2.html', 'w', encoding='utf-8') as f:
    f.write(html_2)

with open('mikado_mkt_3.html', 'w', encoding='utf-8') as f:
    f.write(html_3)

print("Saved HTML templates successfully.")
