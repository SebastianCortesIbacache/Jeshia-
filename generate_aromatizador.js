const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

// ─── DATOS DE AROMAS ────────────────────────────────────────────────────────
const aromasData = [
  { key: 'vainilla-coco',    name: 'VAINILLA COCO',    sub: 'Vainilla Bourbon & Coco',       img: 'vainilla_coco' },
  { key: 'citric',           name: 'CITRIC',            sub: 'Cítricos Frescos & Bergamota',  img: 'citric'        },
  { key: 'berries',          name: 'BERRIES',           sub: 'Frutos Rojos & Silvestres',     img: 'berries'       },
  { key: 'coco-nut',         name: 'COCO NUT',          sub: 'Nuez de Coco & Crema',          img: 'coco_nut'      },
  { key: 'sugar',            name: 'SUGAR',             sub: 'Azúcar Dulce & Caramelo',       img: 'sugar'         },
  { key: 'chicle',           name: 'CHICLE',            sub: 'Bubblegum & Dulce Infancia',    img: 'chicle'        },
  { key: 'manzana-canela',   name: 'MANZANA CANELA',   sub: 'Manzana Asada & Canela',        img: 'manzana_canela'},
  { key: 'coco-flower',      name: 'COCO FLOWER',      sub: 'Flor de Coco & Jazmín',         img: 'coco_flower'   },
  { key: 'mokka',            name: 'MOKKA',             sub: 'Café Moka & Cacao Tostado',     img: 'mokka'         },
  { key: 'limon',            name: 'LIMÓN',             sub: 'Limón Verde',                   img: 'limon'         },
  { key: 'pino',             name: 'PINO',              sub: 'Pino Silvestre & Bosque',       img: 'pino'          },
  { key: 'lavanda',          name: 'LAVANDA',           sub: 'Lavanda Francesa',              img: 'lavanda'       },
  { key: 'frutal-mango',     name: 'FRUTAL MANGO',     sub: 'Mango Tropical',                img: 'frutal_mango'  },
];

// ─── CARGA DE ASSETS (Logo Original Transparente) ───────────────────────────
const logoPath   = path.join(__dirname, 'assets', 'logos', 'Original_Transparent.png');
const logoBase64 = fs.readFileSync(logoPath).toString('base64');
const logoSrc    = `data:image/png;base64,${logoBase64}`;

function loadBotanico(imgKey) {
  const p = path.join(__dirname, 'assets', 'aromas_botanicos', `${imgKey}.png`);
  if (!fs.existsSync(p)) {
    const fb = path.join(__dirname, 'assets', 'aromas_botanicos', 'vainilla_coco.png');
    return `data:image/png;base64,${fs.readFileSync(fb).toString('base64')}`;
  }
  return `data:image/png;base64,${fs.readFileSync(p).toString('base64')}`;
}

// ─── OUTPUT DIR ───────────────────────────────────────────────────────────────
const outDir = path.join(__dirname, 'etiquetas_impresion', '03_Aromatizador_Redonda_Ovalada');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

// ─── HTML GENERATOR CON DISTRIBUCIÓN EXACTA MITAD SUPERIOR / INFERIOR ──────────
function getLabelHtml(aroma, botanicSrc) {
  return `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,400;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      width: 900px;
      height: 900px;
      background: transparent;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    /* ── CÍRCULO PRINCIPAL ────── */
    .label-circle {
      width: 860px;
      height: 860px;
      border-radius: 50%;
      background: #FAF8F5;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;

      /* Borde exterior cobre (#C2825C) idéntico a recargas/mikado */
      border: 5px solid #C2825C;
      box-shadow: inset 0 0 0 7px #FAF8F5, inset 0 0 0 8.5px #C2825C;
    }

    /* Borde interior fino decorativo */
    .label-circle::before {
      content: '';
      position: absolute;
      inset: 16px;
      border-radius: 50%;
      border: 1.2px solid rgba(194, 130, 92, 0.45);
      pointer-events: none;
      z-index: 5;
    }

    /* Marca de registro superior */
    .reg-mark-top {
      position: absolute;
      top: 24px;
      left: 50%;
      transform: translateX(-50%);
      color: #C2825C;
      font-size: 16px;
      font-weight: 300;
      z-index: 6;
      line-height: 1;
    }

    /* Marca de registro inferior */
    .reg-mark-bottom {
      position: absolute;
      bottom: 22px;
      left: 50%;
      transform: translateX(-50%);
      color: #C2825C;
      font-size: 14px;
      opacity: 0.8;
      z-index: 6;
    }

    /* ── MITAD SUPERIOR (LOGO + AROMATIZADOR 15 ML) ───────── */
    .top-half {
      width: 100%;
      height: 430px; /* Exactamente la mitad superior */
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding-top: 30px;
      padding-bottom: 5px;
      position: relative;
      z-index: 3;
    }

    .logo-img {
      width: 355px; /* Logo más grande para presencia en 25mm */
      height: auto;
      object-fit: contain;
    }

    /* SEPARADOR CENTRAL DE CATEGORÍA */
    .middle-divider {
      width: 84%;
      position: relative;
      z-index: 3;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }

    .category-text {
      font-family: 'Montserrat', sans-serif;
      font-size: 24px; /* Mayor tamaño para etiquetas pequeñas de 25mm */
      font-weight: 700;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #C2825C;
      text-align: center;
      padding: 2px 0;
    }

    .hairline {
      width: 100%;
      height: 1.5px;
      background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(194, 130, 92, 0.4) 15%,
        rgba(194, 130, 92, 0.8) 50%,
        rgba(194, 130, 92, 0.4) 85%,
        transparent 100%
      );
    }

    .reg-cross {
      font-size: 13px;
      color: #C2825C;
      opacity: 0.7;
      line-height: 1;
      font-weight: 300;
      margin-top: 1px;
    }

    /* ── MITAD INFERIOR (ILUSTRACIÓN + TEXTO DEL AROMA) ───────── */
    .bottom-half {
      width: 100%;
      height: 430px; /* Exactamente la mitad inferior */
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding-bottom: 25px;
    }

    /* Ilustración botánica de fondo con opacidad */
    .botanical-bg {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 620px;
      height: 370px;
      object-fit: contain;
      opacity: 0.35;
      filter: sepia(75%) saturate(0.75) hue-rotate(-10deg) brightness(0.9);
      z-index: 1;
    }

    /* Contenedor de texto del aroma (Superpuesto en el medio de la ilustración) */
    .aroma-text-container {
      position: relative;
      z-index: 4;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 0 40px;
    }

    /* Nombre del aroma con tono cobre oscuro (#854425) */
    .aroma-name {
      font-family: 'Cormorant Garamond', serif;
      font-size: 72px;
      font-weight: 700;
      color: #854425; /* Cobre oscuro elegante, derivado de #C2825C */
      letter-spacing: 0.05em;
      text-align: center;
      line-height: 1.05;
      text-transform: uppercase;
      text-shadow: 0 0 15px rgba(250, 248, 245, 0.85); /* Suave resplandor para legibilidad perfecta sobre ilustración */
    }

    /* Subtítulo del aroma con Cormorant Garamond Italic */
    .aroma-sub {
      font-family: 'Cormorant Garamond', serif;
      font-style: italic;
      font-size: 28px;
      font-weight: 600;
      color: #9C5634; /* Cobre medio cálido */
      text-align: center;
      margin-top: 8px;
      text-shadow: 0 0 12px rgba(250, 248, 245, 0.85);
    }
  </style>
</head>
<body>
  <div class="label-circle">

    <!-- Marca de registro superior -->
    <div class="reg-mark-top">+</div>

    <!-- 1. MITAD SUPERIOR: LOGO ORIGINAL TRANSPARENTE + FORMATO AROMATIZADOR 15 ML -->
    <div class="top-half">
      <img src="${logoSrc}" alt="Jeshia Logo" class="logo-img">

      <div class="middle-divider">
        <div class="hairline"></div>
        <div class="category-text">AROMATIZADOR &bull; 15 ML</div>
        <div class="hairline"></div>
        <div class="reg-cross">+</div>
      </div>
    </div>

    <!-- 2. MITAD INFERIOR: ILUSTRACIÓN DE FONDO CON TEXTO DE AROMA ENCIMA Y AL MEDIO -->
    <div class="bottom-half">
      <!-- Ilustración botánica de fondo -->
      <img src="${botanicSrc}" alt="Ilustración ${aroma.name}" class="botanical-bg">

      <!-- Texto principal del aroma en el medio de la ilustración -->
      <div class="aroma-text-container">
        <div class="aroma-name">${aroma.name}</div>
        <div class="aroma-sub">${aroma.sub}</div>
      </div>
    </div>

    <!-- Marca de registro inferior -->
    <div class="reg-mark-bottom">•</div>

  </div>
</body>
</html>`;
}

// ─── MAIN GENERATOR ───────────────────────────────────────────────────────────
async function run() {
  console.log('🌸 Generando 13 etiquetas circulares de Aromatizador (Cobre Oscuro + Distribución 50/50)...\n');

  const browser = await puppeteer.launch({
    executablePath: EDGE_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(60000);
  await page.setViewport({ width: 900, height: 900, deviceScaleFactor: 3 });

  // Pre-cargar fuentes
  await page.setContent(`<!DOCTYPE html><html><head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,400;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    </head><body><p style="font-family:'Cormorant Garamond';">x</p><p style="font-family:'Montserrat';">x</p></body></html>`, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  console.log('  Fuentes precargadas correctamente.');

  let count = 0;

  for (const aroma of aromasData) {
    const botanicSrc = loadBotanico(aroma.img);
    const html = getLabelHtml(aroma, botanicSrc);

    await page.setContent(html, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 600));

    const filename = `Aromatizador_${aroma.key.replace(/-/g, '_')}.png`;
    const outPath  = path.join(outDir, filename);

    const el = await page.$('.label-circle');
    await el.screenshot({ path: outPath, type: 'png', omitBackground: true });

    count++;
    console.log(`  ✅ [${count}/13] ${filename}`);
  }

  await browser.close();
  console.log(`\n🎉 ¡Listo! ${count} etiquetas guardadas en:\n   ${outDir}`);
}

run().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
