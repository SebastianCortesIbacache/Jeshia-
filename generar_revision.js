const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

const aromasData = [
  { key: "vainilla_coco",    name: "Vainilla Coco",   sub: "Vainilla Bourbon & Coco" },
  { key: "citric",           name: "Citric",           sub: "Cítricos Frescos & Bergamota" },
  { key: "berries",          name: "Berries",          sub: "Frutos Rojos & Silvestres" },
  { key: "coco_nut",         name: "Coco Nut",         sub: "Nuez de Coco & Crema" },
  { key: "sugar",            name: "Sugar",            sub: "Azúcar Dulce & Caramelo" },
  { key: "chicle",           name: "Chicle",           sub: "Bubblegum & Dulce Infancia" },
  { key: "manzana_canela",   name: "Manzana Canela",   sub: "Manzana Asada & Canela" },
  { key: "coco_flower",      name: "Coco Flower",      sub: "Flor de Coco & Jazmín" },
  { key: "mokka",            name: "Mokka",            sub: "Café Moka & Cacao Tostado" },
  { key: "limon",            name: "Limón",            sub: "Limón Verde" },
  { key: "pino",             name: "Pino",             sub: "Pino Silvestre & Bosque" },
  { key: "lavanda",          name: "Lavanda",          sub: "Lavanda Francesa" },
  { key: "frutal_mango",     name: "Frutal Mango",     sub: "Mango Tropical" },
];

// Load logo
const logoBase64 = fs.readFileSync(path.join(__dirname, 'assets', 'logos', 'Original_Transparent.png')).toString('base64');
const logoSrc = `data:image/png;base64,${logoBase64}`;

// Load botanical images - check aromas_botanicos first, fallback to aromas
function getAromaImg(key) {
  const dirs = [
    path.join(__dirname, 'assets', 'aromas_botanicos'),
    path.join(__dirname, 'assets', 'aromas'),
  ];
  for (const dir of dirs) {
    const p = path.join(dir, key + '.png');
    if (fs.existsSync(p)) {
      return `data:image/png;base64,${fs.readFileSync(p).toString('base64')}`;
    }
  }
  // fallback to vainilla_coco
  const fb = path.join(__dirname, 'assets', 'aromas_botanicos', 'vainilla_coco.png');
  if (fs.existsSync(fb)) return `data:image/png;base64,${fs.readFileSync(fb).toString('base64')}`;
  return null;
}

const outMikado   = path.join(__dirname, 'revision_manual', 'Mikado');
const outVertical = path.join(__dirname, 'revision_manual', 'Vertical');

// ── SVG ornaments ─────────────────────────────────────────────────────────────
const flowerSvgLg = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="2.5" fill="#C2825C"/>
  <path d="M12 3C10.5 6 10.5 8.5 12 9.5C13.5 8.5 13.5 6 12 3Z" fill="#C2825C"/>
  <path d="M12 21C10.5 18 10.5 15.5 12 14.5C13.5 15.5 13.5 18 12 21Z" fill="#C2825C"/>
  <path d="M3 12C6 10.5 8.5 10.5 9.5 12C8.5 13.5 6 13.5 3 12Z" fill="#C2825C"/>
  <path d="M21 12C18 10.5 15.5 10.5 14.5 12C15.5 13.5 18 13.5 21 12Z" fill="#C2825C"/>
</svg>`;

const flowerSvgSm = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="2.5" fill="#C2825C"/>
  <path d="M12 3C10.5 6 10.5 8.5 12 9.5C13.5 8.5 13.5 6 12 3Z" fill="#C2825C"/>
  <path d="M12 21C10.5 18 10.5 15.5 12 14.5C13.5 15.5 13.5 18 12 21Z" fill="#C2825C"/>
  <path d="M3 12C6 10.5 8.5 10.5 9.5 12C8.5 13.5 6 13.5 3 12Z" fill="#C2825C"/>
  <path d="M21 12C18 10.5 15.5 10.5 14.5 12C15.5 13.5 18 13.5 21 12Z" fill="#C2825C"/>
</svg>`;

// ─────────────────────────────────────────────────────────────────────────────
// MIKADO LABEL  50mm x 25mm → 700x350px @3x
// Layout reference: logo top-center, then flower divider, then aroma LEFT + illustration RIGHT
// ─────────────────────────────────────────────────────────────────────────────
function getMikadoHtml(aroma, aromaImgSrc) {
  return `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { width: 700px; height: 350px; background: #ffffff; overflow: hidden; }

    .label {
      width: 700px; height: 350px;
      background: #FAF8F5;
      border: 4px solid #C2825C;
      position: relative;
      display: flex; flex-direction: column;
      align-items: center;
      overflow: hidden;
    }
    .label::before {
      content: ''; position: absolute;
      top: 5px; left: 5px; right: 5px; bottom: 5px;
      border: 1px solid rgba(194,130,92,0.45);
      pointer-events: none; z-index: 1;
    }

    /* Fixed sections */
    .sec-top    { height: 16px; display: flex; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; }
    .sec-logo   { height: 134px; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; }
    .sec-div    { height: 14px; display: flex; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; margin-top: 2px; }
    /* Bottom: flex-row con ilustración junta al texto (gap leve) y centrados */
    .sec-bottom { flex: 1; display: flex; flex-direction: row; align-items: center; justify-content: center; width: 92%; padding: 2px 10px 0 10px; min-height: 0; gap: 22px; }
    .sec-foot   { height: 16px; display: flex; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; }

    /* Dividers */
    .div-dots { display: flex; align-items: center; width: 86%; }
    .div-dots .dot  { width: 5px; height: 5px; background: #C2825C; border-radius: 50%; flex-shrink: 0; }
    .div-dots .line { flex: 1; height: 1px; background: rgba(194,130,92,0.6); }
    .div-flower { display: flex; align-items: center; width: 86%; gap: 8px; }
    .div-flower .line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(194,130,92,0.6) 50%, transparent); }
    .div-center { display: flex; align-items: center; width: 86%; }
    .div-center .line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(194,130,92,0.55) 50%, transparent); }
    .div-center .dot { width: 5px; height: 5px; background: #C2825C; border-radius: 50%; flex-shrink: 0; }

    /* Logo */
    .logo-img { max-height: 103px; max-width: 40%; object-fit: contain; }
    .brand-sub { font-family: 'Montserrat', sans-serif; font-size: 7.9px; letter-spacing: 0.22em; text-transform: uppercase; color: #8c8273; margin-top: 4px; }
    .cat-tag   { font-family: 'Montserrat', sans-serif; font-size: 8.85px; letter-spacing: 0.18em; text-transform: uppercase; color: #C2825C; font-weight: 700; margin-top: 3px; }

    /* Text col & illustration col: pegados con leve gap */
    .text-col { flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
    .aroma-title { font-family: 'Cormorant Garamond', serif; font-size: 2.15rem; font-weight: 700; text-transform: uppercase; color: #23201B; letter-spacing: 0.03em; line-height: 1.05; }
    .aroma-sub   { font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 1.05rem; color: #555046; margin-top: 3px; }

    .ill-col { flex: 0 0 auto; display: flex; align-items: center; justify-content: center; }
    .botanical-img { max-height: 110px; max-width: 150px; object-fit: contain; display: block; }
  </style>
</head>
<body>
  <div class="label">

    <div class="sec-top">
      <div class="div-dots">
        <div class="dot"></div><div class="line"></div><div class="dot"></div>
      </div>
    </div>

    <div class="sec-logo">
      <img src="${logoSrc}" class="logo-img" alt="Logo Jeshia">
      <div class="brand-sub">HOME &amp; AROMAS</div>
      <div class="cat-tag">MIKADO • 50 ML</div>
    </div>

    <div class="sec-div">
      <div class="div-flower">
        <div class="line"></div>${flowerSvgSm}<div class="line"></div>
      </div>
    </div>

    <div class="sec-bottom">
      <div class="text-col">
        <div class="aroma-title">${aroma.name.toUpperCase()}</div>
        <div class="aroma-sub">${aroma.sub}</div>
      </div>
      ${aromaImgSrc ? `<div class="ill-col"><img src="${aromaImgSrc}" class="botanical-img" alt=""></div>` : ''}
    </div>

    <div class="sec-foot">
      <div class="div-center">
        <div class="line"></div><div class="dot"></div><div class="line"></div>
      </div>
    </div>

  </div>
</body>
</html>`;
}

// ─────────────────────────────────────────────────────────────────────────────
// VERTICAL LABEL  Home Spray / Recarga 250 / Recarga 500
// Reference proportions (% of total height):
//   top-div: ~3%, logo+texts: ~28%, mid-div: ~4%, aroma text: ~12%, illustration: ~42%, bot-div: ~3%, footer: ~8%
// ─────────────────────────────────────────────────────────────────────────────
function getVerticalHtml(aroma, aromaImgSrc, spec) {
  const ph = spec.ph;
  // Compute pixel heights for each fixed section
  const topDivH   = Math.round(ph * 0.030);
  const logoH     = Math.round(ph * 0.290);
  const midDivH   = Math.round(ph * 0.038);
  const botDivH   = Math.round(ph * 0.030);
  const footerH   = Math.round(ph * 0.075);
  // sec-content (aroma + illustration) fills all remaining height

  const logoImgH  = Math.round(logoH * 0.86);      // +20% respecto a 0.72
  const brandPx   = Math.round(spec.pw * 0.0154);  // +10% respecto a 0.014
  const catPx     = Math.round(spec.pw * 0.024);   // +20% adicional
  const titlePx   = Math.round(spec.pw * 0.072);
  const subPx     = Math.round(spec.pw * 0.035);
  const footerPx  = Math.round(spec.pw * 0.019);

  return `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { width: ${spec.pw}px; height: ${ph}px; background: #ffffff; overflow: hidden; }

    .label {
      width: ${spec.pw}px; height: ${ph}px;
      background: #FAF8F5;
      border: 4px solid #C2825C;
      position: relative;
      display: flex; flex-direction: column;
      align-items: center;
      overflow: hidden;
    }
    .label::before {
      content: ''; position: absolute;
      top: 5px; left: 5px; right: 5px; bottom: 5px;
      border: 1px solid rgba(194,130,92,0.42);
      pointer-events: none; z-index: 1;
    }

    /* ── Fixed-height sections ── */
    .sec-topdiv  { height: ${topDivH}px;  display: flex; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; }
    .sec-logo    { height: ${logoH}px;    display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; }
    .sec-middiv  { height: ${midDivH}px;  display: flex; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; }
    /* Aroma + illustration together, vertically centered in remaining space */
    .sec-content { flex: 1; min-height: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; gap: 18px; padding: 12px 0; }
    .sec-botdiv  { height: ${botDivH}px;  display: flex; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; }
    .sec-footer  { height: ${footerH}px;  display: flex; align-items: center; justify-content: center; width: 100%; flex-shrink: 0; border-top: 1px solid rgba(194,130,92,0.4); }

    /* ── Dividers ── */
    .div-flower { display: flex; align-items: center; width: 82%; gap: 8px; }
    .div-flower .line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(194,130,92,0.65) 50%, transparent); }
    .div-dot    { display: flex; align-items: center; width: 82%; }
    .div-dot .line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(194,130,92,0.55) 50%, transparent); }
    .div-dot .dot  { width: 5px; height: 5px; background: #C2825C; border-radius: 50%; flex-shrink: 0; }

    /* ── Logo ── */
    .logo-img  { max-height: ${logoImgH}px; max-width: 76%; object-fit: contain; }
    .brand-sub { font-family: 'Montserrat', sans-serif; font-size: ${brandPx}px; letter-spacing: 0.2em; text-transform: uppercase; color: #8c8273; margin-top: 5px; }
    .cat-tag   { font-family: 'Montserrat', sans-serif; font-size: ${catPx}px; letter-spacing: 0.16em; text-transform: uppercase; color: #C2825C; font-weight: 700; margin-top: 3px; }

    /* ── Aroma text ── */
    .aroma-title { font-family: 'Cormorant Garamond', serif; font-size: ${titlePx}px; font-weight: 700; text-transform: uppercase; color: #23201B; letter-spacing: 0.03em; line-height: 1; }
    .aroma-sub   { font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: ${subPx}px; color: #555046; margin-top: 4px; }

    /* ── Aroma text block ── */
    .aroma-block { display: flex; flex-direction: column; align-items: center; text-align: center; }

    /* ── Ilustración vertical ── */
    .botanical-img { max-width: 38%; max-height: 205px; object-fit: contain; display: block; }

    /* ── Footer ── */
    .footer-txt { font-family: 'Montserrat', sans-serif; font-size: ${footerPx}px; letter-spacing: 0.03em; color: #554f46; text-align: center; }
  </style>
</head>
<body>
  <div class="label">

    <div class="sec-topdiv">
      <div class="div-flower"><div class="line"></div>${flowerSvgLg}<div class="line"></div></div>
    </div>

    <div class="sec-logo">
      <img src="${logoSrc}" class="logo-img" alt="Logo Jeshia">
      <div class="brand-sub">HOME &amp; AROMAS</div>
      <div class="cat-tag">${spec.catText}</div>
    </div>

    <div class="sec-middiv">
      <div class="div-dot"><div class="line"></div><div class="dot"></div><div class="line"></div></div>
    </div>

    <div class="sec-content">
      <div class="aroma-block">
        <div class="aroma-title">${aroma.name.toUpperCase()}</div>
        <div class="aroma-sub">${aroma.sub}</div>
      </div>
      ${aromaImgSrc ? `<img src="${aromaImgSrc}" class="botanical-img" alt="">` : ''}
    </div>

    <div class="sec-botdiv">
      <div class="div-dot"><div class="line"></div><div class="dot"></div><div class="line"></div></div>
    </div>

    <div class="sec-footer">
      <div class="footer-txt">WhatsApp: +56 9 3114 1134 / +56 9 3362 0641 | TikTok: @jeshiacybn</div>
    </div>

  </div>
</body>
</html>`;
}

// ─────────────────────────────────────────────────────────────────────────────
// PRODUCT SPECS
// ─────────────────────────────────────────────────────────────────────────────
const verticalProducts = [
  { prefix: 'HomeSpray_250ml',   catText: 'HOME SPRAY • 250 ML',       pw: 660, ph: 860  },
  { prefix: 'Recarga_250ml',     catText: 'RECARGA ECO • 250 ML',       pw: 660, ph: 860  },
  { prefix: 'Recarga_500ml',     catText: 'RECARGA FAMILIAR • 500 ML',  pw: 660, ph: 1130 },
];

// ─────────────────────────────────────────────────────────────────────────────
// MAIN
// ─────────────────────────────────────────────────────────────────────────────
async function run() {
  const browser = await puppeteer.launch({
    executablePath: EDGE_PATH, headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  // ── MIKADO ────────────────────────────────────────────────────────────────
  console.log('\n📌 MIKADO labels (13)...');
  {
    const page = await browser.newPage();
    await page.setViewport({ width: 700, height: 350, deviceScaleFactor: 3 });

    const extraDir = path.join(__dirname, 'etiquetas_impresion', '01_Mikado_50x25mm');
    if (!fs.existsSync(extraDir)) fs.mkdirSync(extraDir, { recursive: true });

    for (const aroma of aromasData) {
      const html = getMikadoHtml(aroma, getAromaImg(aroma.key));
      await page.setContent(html, { waitUntil: 'domcontentloaded' });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 400));

      const outPath = path.join(outMikado, `Mikado_${aroma.key}.png`);
      const extraPath = path.join(extraDir, `Mikado_${aroma.key}.png`);
      const el = await page.$('.label');
      await el.screenshot({ path: outPath, type: 'png' });
      await el.screenshot({ path: extraPath, type: 'png' });
      console.log(`  ✓ ${aroma.name}`);
    }
    await page.close();
  }

  // ── VERTICAL LABELS ───────────────────────────────────────────────────────
  console.log('\n📌 VERTICAL labels (Home Spray + Recargas)...');
  for (const spec of verticalProducts) {
    const page = await browser.newPage();
    await page.setViewport({ width: spec.pw, height: spec.ph, deviceScaleFactor: 3 });

    let extraFolder = '';
    let extraFilePrefix = spec.prefix;
    if (spec.prefix === 'HomeSpray_250ml') {
      extraFolder = '02_Home_Spray_60x75mm';
      extraFilePrefix = 'Home_Spray';
    } else if (spec.prefix === 'Recarga_250ml') {
      extraFolder = '04_Recarga_250ml_60x75mm';
    } else if (spec.prefix === 'Recarga_500ml') {
      extraFolder = '05_Recarga_500ml_60x100mm';
    }
    const extraDir = extraFolder ? path.join(__dirname, 'etiquetas_impresion', extraFolder) : null;
    if (extraDir && !fs.existsSync(extraDir)) fs.mkdirSync(extraDir, { recursive: true });

    for (const aroma of aromasData) {
      const html = getVerticalHtml(aroma, getAromaImg(aroma.key), spec);
      await page.setContent(html, { waitUntil: 'domcontentloaded' });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 400));

      const outPath = path.join(outVertical, `${spec.prefix}_${aroma.key}.png`);
      const el = await page.$('.label');
      await el.screenshot({ path: outPath, type: 'png' });

      if (extraDir) {
        const extraPath = path.join(extraDir, `${extraFilePrefix}_${aroma.key}.png`);
        await el.screenshot({ path: extraPath, type: 'png' });
      }

      console.log(`  ✓ ${spec.prefix} / ${aroma.name}`);
    }
    await page.close();
  }

  await browser.close();
  console.log('\n🎉 Done! Labels saved to revision_manual/ and etiquetas_impresion/');
}

run().catch(err => { console.error(err); process.exit(1); });
