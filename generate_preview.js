const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

const logoPath = path.join(__dirname, 'assets', 'logos', 'Original_Transparent.png');
const logoBase64 = fs.readFileSync(logoPath).toString('base64');
const logoSrc = `data:image/png;base64,${logoBase64}`;

const vainillaImgPath = path.join(__dirname, 'assets', 'aromas', 'vainilla_coco.png');
const vainillaBase64 = fs.readFileSync(vainillaImgPath).toString('base64');
const vainillaSrc = `data:image/png;base64,${vainillaBase64}`;

const citricImgPath = path.join(__dirname, 'assets', 'aromas', 'citric.png');
const citricBase64 = fs.readFileSync(citricImgPath).toString('base64');
const citricSrc = `data:image/png;base64,${citricBase64}`;

function getPreviewHtml() {
  return `
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #EFECE6;
      display: flex;
      gap: 50px;
      align-items: center;
      justify-content: center;
      padding: 40px;
      font-family: 'Montserrat', sans-serif;
    }

    /* CARD CONTAINER WITH DOUBLE BORDER */
    .label-card {
      background: #FAF8F5;
      border: 3.5px solid #C2825C;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      text-align: center;
      color: #2A2723;
      box-shadow: 0 16px 45px rgba(0,0,0,0.12);
    }

    .label-card::before {
      content: '';
      position: absolute;
      top: 5px; left: 5px; right: 5px; bottom: 5px;
      border: 1px solid rgba(194, 130, 92, 0.45);
      pointer-events: none;
    }

    /* ORNAMENTAL DIVIDERS */
    .divider-dots-line {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 84%;
      margin: 2px 0;
    }
    .divider-dots-line .dot {
      width: 4.5px;
      height: 4.5px;
      background-color: #C2825C;
      border-radius: 50%;
    }
    .divider-dots-line .line {
      flex: 1;
      height: 1px;
      background: #C2825C;
      opacity: 0.55;
    }

    .divider-center-dot {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 84%;
      gap: 10px;
      margin: 2px 0;
    }
    .divider-center-dot .line {
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, rgba(194,130,92,0.05) 0%, rgba(194,130,92,0.6) 50%, rgba(194,130,92,0.05) 100%);
    }
    .divider-center-dot .dot {
      width: 4.5px;
      height: 4.5px;
      background-color: #C2825C;
      border-radius: 50%;
    }

    .divider-flower {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 84%;
      gap: 10px;
      margin: 2px 0;
    }
    .divider-flower .line {
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, rgba(194,130,92,0.05) 0%, rgba(194,130,92,0.65) 50%, rgba(194,130,92,0.05) 100%);
    }

    .logo-img {
      object-fit: contain;
    }

    .brand-subhead {
      font-size: 0.65rem;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #8c8273;
      margin-top: 2px;
    }

    .cat-tag {
      font-size: 0.72rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #C2825C;
      font-weight: 700;
      margin-top: 1px;
    }

    .aroma-title {
      font-family: 'Cormorant Garamond', serif;
      font-weight: 700;
      text-transform: uppercase;
      line-height: 1.05;
      color: #23201B;
      letter-spacing: 0.05em;
    }

    .aroma-sub {
      font-family: 'Cormorant Garamond', serif;
      font-style: italic;
      color: #555046;
    }

    .botanical-img {
      object-fit: contain;
    }

    .footer-box {
      width: 100%;
      font-size: 0.68rem;
      letter-spacing: 0.04em;
      color: #554f46;
      border-top: 1px solid rgba(194, 130, 92, 0.4);
      padding-top: 5px;
    }
  </style>
</head>
<body>

  <!-- PREVIEW 1: MIKADO 50 ML (EXACT PROPORTIONAL DESIGN MATCHING USER IMAGE 1) -->
  <div class="label-card" style="width: 590px; height: 295px; padding: 14px 22px;">
    <!-- TOP LINE WITH DOT ENDINGS •─────────• -->
    <div class="divider-dots-line" style="width: 82%;">
      <div class="dot"></div>
      <div class="line"></div>
      <div class="dot"></div>
    </div>

    <!-- LOGO & BRAND (PROPORTIONAL SIZING MATCHING IMAGE 1) -->
    <div style="display:flex; flex-direction:column; align-items:center; width:100%;">
      <img src="${logoSrc}" class="logo-img" style="max-height: 68px; width: 34%;">
      <div class="brand-subhead" style="font-size:0.62rem; margin-top:3px;">HOME & AROMAS</div>
      <div class="cat-tag" style="font-size:0.68rem; margin-top:2px;">MIKADO • 50 ML</div>
    </div>

    <!-- MIDDLE FLOWER DIVIDER -->
    <div class="divider-flower" style="width: 82%;">
      <div class="line"></div>
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="2.5" fill="#C2825C"/>
        <path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/>
        <path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/>
        <path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/>
        <path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/>
      </svg>
      <div class="line"></div>
    </div>

    <!-- BOTTOM ROW: LEFT TEXT + RIGHT ILLUSTRATION -->
    <div style="width:94%; display:flex; align-items:center; justify-content:space-between; padding:0 5px;">
      <div style="text-align:left;">
        <h2 class="aroma-title" style="font-size: 1.85rem;">VAINILLA COCO</h2>
        <div class="aroma-sub" style="font-size: 1.1rem; margin-top:2px;">Vainilla Bourbon & Coco</div>
      </div>
      <img src="${vainillaSrc}" class="botanical-img" style="max-height: 90px; max-width: 170px;">
    </div>

    <!-- BOTTOM LINE WITH CENTER DOT ────•──── -->
    <div class="divider-center-dot" style="width: 82%; margin-bottom:2px;">
      <div class="line"></div>
      <div class="dot"></div>
      <div class="line"></div>
    </div>
  </div>


  <!-- PREVIEW 2: HOME SPRAY 250 ML / RECARGAS (PROPORTIONAL & PROMINENT LOGO, 100% TRANSPARENT ILLUSTRATION, 2 PHONES) -->
  <div class="label-card" style="width: 500px; height: 680px; padding: 22px 25px;">
    <!-- TOP FLOWER DIVIDER -->
    <div class="divider-flower" style="width: 82%;">
      <div class="line"></div>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="2.5" fill="#C2825C"/>
        <path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/>
        <path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/>
        <path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/>
        <path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/>
      </svg>
      <div class="line"></div>
    </div>

    <!-- LOGO & BRAND (PROMINENT LOGO - HIGH PROPORTION OVER ILLUSTRATION) -->
    <div style="display:flex; flex-direction:column; align-items:center; width:100%;">
      <img src="${logoSrc}" class="logo-img" style="max-height: 195px; width: 85%;">
      <div class="brand-subhead" style="font-size:0.75rem; margin-top:4px;">HOME & AROMAS</div>
      <div class="cat-tag" style="font-size:0.8rem; margin-top:3px;">HOME SPRAY • 250 ML</div>
    </div>

    <!-- MIDDLE FLOWER DIVIDER -->
    <div class="divider-flower" style="width: 82%;">
      <div class="line"></div>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="2.5" fill="#C2825C"/>
        <path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/>
        <path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/>
        <path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/>
        <path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/>
      </svg>
      <div class="line"></div>
    </div>

    <!-- TITLE & SUBTITLE -->
    <div style="width:100%;">
      <h2 class="aroma-title" style="font-size: 2.3rem;">CITRIC</h2>
      <div class="aroma-sub" style="font-size: 1.15rem; margin-top:1px;">Cítricos Frescos & Bergamota</div>
    </div>

    <!-- BOTANICAL ILLUSTRATION (100% ISOLATED TRANSPARENT WREATH) -->
    <img src="${citricSrc}" class="botanical-img" style="max-height: 145px; width: 58%;">

    <!-- BOTTOM CENTER DOT DIVIDER -->
    <div class="divider-center-dot" style="width: 82%;">
      <div class="line"></div>
      <div class="dot"></div>
      <div class="line"></div>
    </div>

    <!-- FOOTER WITH 2 WHATSAPP NUMBERS -->
    <div class="footer-box">
      WhatsApp: +56 9 3114 1134 / +56 9 3362 0641 | TikTok: @jeshiacybn
    </div>
  </div>

</body>
</html>
  `;
}

async function run() {
  const browser = await puppeteer.launch({
    executablePath: EDGE_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setContent(getPreviewHtml(), { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 1200));

  await page.setViewport({ width: 1220, height: 790, deviceScaleFactor: 2 });

  const previewPath = path.join(__dirname, 'preview_diseno_nuevo.png');
  await page.screenshot({ path: previewPath, fullPage: true });

  await browser.close();
  console.log("Updated preview created successfully at: " + previewPath);
}

run().catch(console.error);
