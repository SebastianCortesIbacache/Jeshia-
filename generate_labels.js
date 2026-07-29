const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

const aromasData = {
  "vainilla-coco": { name: "Vainilla Coco", sub: "Vainilla Bourbon & Coco", imgKey: "vainilla_coco" },
  "citric": { name: "Citric", sub: "Cítricos Frescos & Bergamota", imgKey: "citric" },
  "berries": { name: "Berries", sub: "Frutos Rojos & Silvestres", imgKey: "berries" },
  "coco-nut": { name: "Coco Nut", sub: "Nuez de Coco & Crema", imgKey: "coco_nut" },
  "sugar": { name: "Sugar", sub: "Azúcar Dulce & Caramelo", imgKey: "sugar" },
  "chicle": { name: "Chicle", sub: "Bubblegum & Dulce Infancia", imgKey: "chicle" },
  "manzana-canela": { name: "Manzana Canela", sub: "Manzana Asada & Canela", imgKey: "manzana_canela" },
  "coco-flower": { name: "Coco Flower", sub: "Flor de Coco & Jazmín", imgKey: "coco_flower" },
  "mokka": { name: "Mokka", sub: "Café Moka & Cacao Tostado", imgKey: "mokka" },
  "limon": { name: "Limón", sub: "Limón Verde", imgKey: "limon" },
  "pino": { name: "Pino", sub: "Pino Silvestre & Bosque", imgKey: "pino" },
  "lavanda": { name: "Lavanda", sub: "Lavanda Francesa", imgKey: "lavanda" },
  "frutal-mango": { name: "Frutal Mango", sub: "Mango Tropical", imgKey: "frutal_mango" }
};

const productSpecs = {
  "mikado": {
    folder: "01_Mikado_50x25mm",
    prefix: "Mikado",
    widthMm: 50,
    heightMm: 25,
    pixelW: 700,
    pixelH: 350,
    catText: "MIKADO • 50 ML",
    isCircular: false,
    layoutType: "mikado"
  },
  "spray": {
    folder: "02_Home_Spray_60x75mm",
    prefix: "Home_Spray",
    widthMm: 60,
    heightMm: 75,
    pixelW: 720,
    pixelH: 900,
    catText: "HOME SPRAY • 250 ML",
    isCircular: false,
    layoutType: "vertical",
    footerText: "WhatsApp: +56 9 3114 1134 / +56 9 3362 0641 | TikTok: @jeshiacybn"
  },
  "recarga250": {
    folder: "04_Recarga_250ml_60x75mm",
    prefix: "Recarga_250ml",
    widthMm: 60,
    heightMm: 75,
    pixelW: 720,
    pixelH: 900,
    catText: "RECARGA ECO • 250 ML",
    isCircular: false,
    layoutType: "vertical",
    footerText: "WhatsApp: +56 9 3114 1134 / +56 9 3362 0641 | TikTok: @jeshiacybn"
  },
  "recarga500": {
    folder: "05_Recarga_500ml_60x100mm",
    prefix: "Recarga_500ml",
    widthMm: 60,
    heightMm: 100,
    pixelW: 720,
    pixelH: 1200,
    catText: "RECARGA FAMILIAR • 500 ML",
    isCircular: false,
    layoutType: "vertical",
    footerText: "WhatsApp: +56 9 3114 1134 / +56 9 3362 0641 | TikTok: @jeshiacybn"
  },
  "crema": {
    folder: "06_Crema_60x40mm",
    prefix: "Crema",
    widthMm: 60,
    heightMm: 40,
    pixelW: 720,
    pixelH: 480,
    catText: "CREMA CORPORAL • 100 G",
    isCircular: false,
    layoutType: "horizontal",
    footerText: ""
  },
  "aromatizador": {
    folder: "03_Aromatizador_Redonda_Ovalada",
    prefix: "Aromatizador",
    widthMm: 45,
    heightMm: 45,
    pixelW: 650,
    pixelH: 650,
    catText: "AROMATIZADOR • 15 ML",
    isCircular: true,
    layoutType: "circular",
    footerText: ""
  }
};

// Load base logo
const logoPath = path.join(__dirname, 'assets', 'logos', 'Original_Transparent.png');
const logoBase64 = fs.readFileSync(logoPath).toString('base64');
const logoSrc = `data:image/png;base64,${logoBase64}`;

// Load available botanical images
const aromaImages = {};
const aromasDir = path.join(__dirname, 'assets', 'aromas');
if (fs.existsSync(aromasDir)) {
  const files = fs.readdirSync(aromasDir);
  files.forEach(f => {
    if (f.endsWith('.png')) {
      const key = f.replace('.png', '');
      const b64 = fs.readFileSync(path.join(aromasDir, f)).toString('base64');
      aromaImages[key] = `data:image/png;base64,${b64}`;
    }
  });
}

const outBaseDir = path.join(__dirname, 'etiquetas_impresion');
if (!fs.existsSync(outBaseDir)) fs.mkdirSync(outBaseDir, { recursive: true });

Object.values(productSpecs).forEach(spec => {
  const dir = path.join(outBaseDir, spec.folder);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

function getMasterHtml() {
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
      background: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Montserrat', sans-serif;
    }

    /* CARD CONTAINER WITH DOUBLE BORDER */
    .label-card {
      background: #FAF8F5;
      border: 4px solid #C2825C;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      text-align: center;
      color: #2A2723;
    }

    .label-card.rect-card::before {
      content: '';
      position: absolute;
      top: 6px; left: 6px; right: 6px; bottom: 6px;
      border: 1.2px solid rgba(194, 130, 92, 0.45);
      pointer-events: none;
    }

    .label-card.circular-card {
      border-radius: 50%;
      padding: 30px;
    }
    .label-card.circular-card::before {
      content: '';
      position: absolute;
      top: 7px; left: 7px; right: 7px; bottom: 7px;
      border: 1.2px solid rgba(194, 130, 92, 0.45);
      border-radius: 50%;
      pointer-events: none;
    }

    /* DIVIDER STYLES */
    .divider-dots-line {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 84%;
      margin: 2px 0;
    }
    .divider-dots-line .dot {
      width: 5px;
      height: 5px;
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
      width: 5px;
      height: 5px;
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
      font-size: 0.68rem;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #8c8273;
      margin-top: 3px;
    }

    .cat-tag {
      font-size: 0.75rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #C2825C;
      font-weight: 700;
      margin-top: 2px;
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
      font-size: 0.72rem;
      letter-spacing: 0.04em;
      color: #554f46;
      border-top: 1px solid rgba(194, 130, 92, 0.4);
      padding-top: 6px;
    }
  </style>
</head>
<body>
  <div id="label-container" class="label-card rect-card"></div>
</body>
</html>
  `;
}

async function run() {
  console.log("Generating 78 Production Print Labels in Ultra HD...");
  const browser = await puppeteer.launch({
    executablePath: EDGE_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setContent(getMasterHtml(), { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 1200));

  let totalGenerated = 0;

  for (const [pKey, spec] of Object.entries(productSpecs)) {
    console.log(`Processing product line: ${spec.folder}...`);

    await page.setViewport({
      width: spec.pixelW,
      height: spec.pixelH,
      deviceScaleFactor: 3
    });

    for (const [aKey, aroma] of Object.entries(aromasData)) {
      const aromaImgSrc = aromaImages[aroma.imgKey] || aromaImages['vainilla_coco'];

      await page.evaluate((spec, aroma, pKey, logoSrc, aromaImgSrc) => {
        const container = document.getElementById('label-container');
        container.style.width = spec.pixelW + 'px';
        container.style.height = spec.pixelH + 'px';
        
        if (spec.isCircular) {
          container.className = 'label-card circular-card';
          container.style.padding = '30px 20px';
          container.innerHTML = `
            <div class="divider-flower" style="width: 80%;">
              <div class="line"></div>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="2.5" fill="#C2825C"/><path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/><path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/><path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/><path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/></svg>
              <div class="line"></div>
            </div>

            <div style="display:flex; flex-direction:column; align-items:center; width:100%;">
              <img src="${logoSrc}" class="logo-img" style="max-height: 140px; width: 80%;">
              <div class="brand-subhead" style="font-size:0.68rem; margin-top:2px;">HOME & AROMAS</div>
              <div class="cat-tag" style="font-size:0.75rem; margin-top:2px;">${spec.catText}</div>
            </div>

            <div class="divider-flower" style="width: 80%;">
              <div class="line"></div>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="2.5" fill="#C2825C"/><path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/><path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/><path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/><path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/></svg>
              <div class="line"></div>
            </div>

            <div style="width:100%;">
              <h2 class="aroma-title" style="font-size: 2.1rem;">${aroma.name}</h2>
              <div class="aroma-sub" style="font-size: 1.1rem; margin-top:1px;">${aroma.sub}</div>
            </div>

            <div class="divider-center-dot" style="width: 80%;">
              <div class="line"></div>
              <div class="dot"></div>
              <div class="line"></div>
            </div>
          `;
        } else if (spec.layoutType === 'mikado') {
          container.className = 'label-card rect-card';
          container.style.padding = '14px 22px';
          container.innerHTML = `
            <div class="divider-dots-line" style="width: 82%;">
              <div class="dot"></div>
              <div class="line"></div>
              <div class="dot"></div>
            </div>

            <div style="display:flex; flex-direction:column; align-items:center; width:100%;">
              <img src="${logoSrc}" class="logo-img" style="max-height: 72px; width: 34%;">
              <div class="brand-subhead" style="font-size:0.62rem; margin-top:3px;">HOME & AROMAS</div>
              <div class="cat-tag" style="font-size:0.68rem; margin-top:2px;">${spec.catText}</div>
            </div>

            <div class="divider-flower" style="width: 82%;">
              <div class="line"></div>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="2.5" fill="#C2825C"/><path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/><path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/><path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/><path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/></svg>
              <div class="line"></div>
            </div>

            <div style="width:94%; display:flex; align-items:center; justify-content:space-between; padding:0 5px;">
              <div style="text-align:left;">
                <h2 class="aroma-title" style="font-size: 1.9rem;">${aroma.name}</h2>
                <div class="aroma-sub" style="font-size: 1.1rem; margin-top:2px;">${aroma.sub}</div>
              </div>
              <img src="${aromaImgSrc}" class="botanical-img" style="max-height: 95px; max-width: 175px;">
            </div>

            <div class="divider-center-dot" style="width: 82%; margin-bottom:2px;">
              <div class="line"></div>
              <div class="dot"></div>
              <div class="line"></div>
            </div>
          `;
        } else {
          // VERTICAL CARDS (HOME SPRAY, RECARGA 250, RECARGA 500)
          container.className = 'label-card rect-card';
          const isRecarga500 = pKey === 'recarga500';
          container.style.padding = isRecarga500 ? '30px 30px' : '22px 25px';

          const logoH = isRecarga500 ? '240px' : '195px';
          const illH = isRecarga500 ? '180px' : '145px';
          const titleFont = isRecarga500 ? '2.7rem' : '2.3rem';

          container.innerHTML = `
            <div class="divider-flower" style="width: 82%;">
              <div class="line"></div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="2.5" fill="#C2825C"/><path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/><path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/><path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/><path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/></svg>
              <div class="line"></div>
            </div>

            <div style="display:flex; flex-direction:column; align-items:center; width:100%;">
              <img src="${logoSrc}" class="logo-img" style="max-height: ${logoH}; width: 85%;">
              <div class="brand-subhead" style="font-size:0.78rem; margin-top:4px;">HOME & AROMAS</div>
              <div class="cat-tag" style="font-size:0.82rem; margin-top:3px;">${spec.catText}</div>
            </div>

            <div class="divider-flower" style="width: 82%;">
              <div class="line"></div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="2.5" fill="#C2825C"/><path d="M12 3C10.5 6 10.5 8 12 9C13.5 8 13.5 6 12 3Z" fill="#C2825C"/><path d="M12 21C10.5 18 10.5 16 12 15C13.5 16 13.5 18 12 21Z" fill="#C2825C"/><path d="M3 12C6 10.5 8 10.5 9 12C8 13.5 6 13.5 3 12Z" fill="#C2825C"/><path d="M21 12C18 10.5 16 10.5 15 12C16 13.5 18 13.5 21 12Z" fill="#C2825C"/></svg>
              <div class="line"></div>
            </div>

            <div style="width:100%;">
              <h2 class="aroma-title" style="font-size: ${titleFont};">${aroma.name}</h2>
              <div class="aroma-sub" style="font-size: 1.18rem; margin-top:1px;">${aroma.sub}</div>
            </div>

            <img src="${aromaImgSrc}" class="botanical-img" style="max-height: ${illH}; width: 58%;">

            <div class="divider-center-dot" style="width: 82%;">
              <div class="line"></div>
              <div class="dot"></div>
              <div class="line"></div>
            </div>

            <div class="footer-box">
              ${spec.footerText}
            </div>
          `;
        }
      }, spec, aroma, pKey, logoSrc, aromaImgSrc);

      await new Promise(r => setTimeout(r, 80));

      const filename = `${spec.prefix}_${aKey.replace(/-/g, '_')}.png`;
      const outPath = path.join(outBaseDir, spec.folder, filename);

      const containerHandle = await page.$('#label-container');
      await containerHandle.screenshot({
        path: outPath,
        type: 'png'
      });

      totalGenerated++;
      console.log(` Saved [${totalGenerated}/78]: ${spec.folder}/${filename}`);
    }
  }

  await browser.close();
  console.log(`🎉 SUCCESS! Generated ${totalGenerated} print labels in 'etiquetas_impresion/'`);
}

run().catch(err => {
  console.error("Error generating labels:", err);
  process.exit(1);
});
