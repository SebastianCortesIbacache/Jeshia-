const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

const baseDir = __dirname;
const montajesBaseDir = path.join(baseDir, 'assets', 'montajes');
const labelsBaseDir   = path.join(baseDir, 'etiquetas_impresion');

const outDir = path.join(baseDir, 'etiquetas_impresion', '00_Montajes_Productos');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

function getBase64(filePath) {
  if (!fs.existsSync(filePath)) return '';
  return `data:image/png;base64,${fs.readFileSync(filePath).toString('base64')}`;
}

const imgMikado = getBase64(path.join(montajesBaseDir, 'Mikado Original.png'));
const imgRecarga500 = getBase64(path.join(montajesBaseDir, 'Recarga 500.png'));
const imgHomeSprayOrig = getBase64(path.join(montajesBaseDir, 'Home Spray Original.png'));
const imgRecarga250 = getBase64(path.join(montajesBaseDir, 'Recarga 250.png'));
const imgAromatizador = getBase64(path.join(montajesBaseDir, 'aromatizador.png'));

const labelMikado = getBase64(path.join(labelsBaseDir, '01_Mikado_50x25mm', 'Mikado_vainilla_coco.png'));
const labelRecarga500 = getBase64(path.join(labelsBaseDir, '05_Recarga_500ml_60x100mm', 'Recarga_500ml_lavanda.png'));
const labelHomeSprayCafe = getBase64(path.join(labelsBaseDir, '02_Home_Spray_60x75mm', 'Home_Spray_coco_flower.png'));
const labelHomeSprayTransp = getBase64(path.join(labelsBaseDir, '02_Home_Spray_60x75mm', 'Home_Spray_manzana_canela.png'));
const labelRecarga250 = getBase64(path.join(labelsBaseDir, '04_Recarga_250ml_60x75mm', 'Recarga_250ml_berries.png'));
const labelAromatizador = getBase64(path.join(labelsBaseDir, '03_Aromatizador_Redonda_Ovalada', 'Aromatizador_coco_nut.png'));

async function renderMontages() {
  console.log('🖼️ Generando montajes finales con tubo interno perfeccionado...\n');

  const browser = await puppeteer.launch({
    executablePath: EDGE_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 1200, deviceScaleFactor: 2 });

  const htmlContent = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { width: 1200px; height: 1200px; background: #FFFFFF; display:flex; align-items:center; justify-content:center; }
    canvas { background: #FFFFFF; }
  </style>
</head>
<body>
  <canvas id="stage" width="1200" height="1200"></canvas>
  <script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');

    function loadImage(src) {
      return new Promise((resolve) => {
        if (!src) return resolve(null);
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = () => resolve(null);
        img.src = src;
      });
    }

    function makeBackgroundTransparent(img, width, height, threshold = 238) {
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = width;
      tempCanvas.height = height;
      const tCtx = tempCanvas.getContext('2d');
      tCtx.drawImage(img, 0, 0, width, height);

      const imgData = tCtx.getImageData(0, 0, width, height);
      const d = imgData.data;

      const visited = new Uint8Array(width * height);
      const queue = [];

      for (let x = 0; x < width; x++) {
        queue.push(x, 0); queue.push(x, height - 1);
      }
      for (let y = 0; y < height; y++) {
        queue.push(0, y); queue.push(width - 1, y);
      }

      while (queue.length > 0) {
        const y = queue.pop();
        const x = queue.pop();
        const idx = y * width + x;

        if (visited[idx]) continue;
        visited[idx] = 1;

        const p = idx * 4;
        const r = d[p], g = d[p+1], b = d[p+2];

        if (r >= threshold && g >= threshold && b >= threshold) {
          d[p+3] = 0;

          if (x > 0) queue.push(x - 1, y);
          if (x < width - 1) queue.push(x + 1, y);
          if (y > 0) queue.push(x, y - 1);
          if (y < height - 1) queue.push(x, y + 1);
        }
      }

      tCtx.putImageData(imgData, 0, 0);
      return tempCanvas;
    }

    // ── 1. MIKADO CON VARILLAS RATTAN ─────────────────────────────
    async function drawMikado(imgBotSrc, imgLblSrc) {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1200, 1200);

      const botRaw = await loadImage(imgBotSrc);
      const lbl = await loadImage(imgLblSrc);

      const botW = 520;
      const botH = 620;
      const botX = (1200 - botW) / 2;
      const botY = 460;

      const botClean = makeBackgroundTransparent(botRaw, botW, botH, 235);

      ctx.save();
      ctx.beginPath();
      ctx.ellipse(600, 1065, 230, 26, 0, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.11)';
      ctx.filter = 'blur(14px)';
      ctx.fill();
      ctx.restore();

      const reeds = [
        { x1: 600, y1: 535, x2: 380, y2: 120, w: 10, c: '#D8B890' },
        { x1: 595, y1: 535, x2: 460, y2: 85,  w: 10, c: '#C8A375' },
        { x1: 600, y1: 535, x2: 545, y2: 60,  w: 11, c: '#E2C29A' },
        { x1: 605, y1: 535, x2: 645, y2: 60,  w: 10, c: '#C49F70' },
        { x1: 605, y1: 535, x2: 730, y2: 90,  w: 10, c: '#D0AC82' },
        { x1: 600, y1: 535, x2: 810, y2: 135, w: 10, c: '#BC9668' },
      ];

      reeds.forEach(r => {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(r.x1, r.y1);
        ctx.lineTo(r.x2, r.y2);
        ctx.lineWidth = r.w;
        ctx.strokeStyle = r.c;
        ctx.lineCap = 'round';
        ctx.shadowColor = 'rgba(0,0,0,0.12)';
        ctx.shadowBlur = 5;
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(r.x1 - 1, r.y1);
        ctx.lineTo(r.x2 - 1, r.y2);
        ctx.lineWidth = r.w * 0.3;
        ctx.strokeStyle = 'rgba(255,255,255,0.4)';
        ctx.stroke();
        ctx.restore();
      });

      ctx.drawImage(botClean, botX, botY);

      if (lbl) {
        const lblW = 280;
        const lblH = 140;
        const lblX = (1200 - lblW) / 2;
        const lblY = botY + 285;

        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,0.2)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetY = 3;
        ctx.drawImage(lbl, lblX, lblY, lblW, lblH);
        ctx.restore();

        ctx.save();
        const grad = ctx.createLinearGradient(lblX, lblY, lblX + lblW, lblY + lblH);
        grad.addColorStop(0, 'rgba(255,255,255,0.14)');
        grad.addColorStop(0.5, 'transparent');
        grad.addColorStop(1, 'rgba(0,0,0,0.06)');
        ctx.fillStyle = grad;
        ctx.fillRect(lblX, lblY, lblW, lblH);
        ctx.restore();
      }

      return canvas.toDataURL('image/png');
    }

    // ── 2. RECARGA 500 ML ──────────────────────────────────────────
    async function drawRecarga500(imgBotSrc, imgLblSrc) {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1200, 1200);

      const botRaw = await loadImage(imgBotSrc);
      const lbl = await loadImage(imgLblSrc);

      const botW = 380;
      const botH = 990;
      const botX = (1200 - botW) / 2;
      const botY = 110;

      const botClean = makeBackgroundTransparent(botRaw, botW, botH, 235);

      const bCtx = botClean.getContext('2d');
      const imgData = bCtx.getImageData(0, 0, botW, botH);
      const d = imgData.data;

      for (let i = 0; i < d.length; i += 4) {
        if (d[i+3] > 10) {
          const r = d[i], g = d[i+1], b = d[i+2];
          if (r > 140 && g > 130 && b < 140) {
            const lum = (r * 0.3 + g * 0.59 + b * 0.11) / 255;
            d[i]   = Math.min(255, Math.floor(210 * lum + 25));
            d[i+1] = Math.min(255, Math.floor(150 * lum + 15));
            d[i+2] = Math.min(255, Math.floor(80  * lum + 10));
          }
        }
      }
      bCtx.putImageData(imgData, 0, 0);

      ctx.save();
      ctx.beginPath();
      ctx.ellipse(600, 1090, 180, 22, 0, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.14)';
      ctx.filter = 'blur(12px)';
      ctx.fill();
      ctx.restore();

      ctx.drawImage(botClean, botX, botY);

      if (lbl) {
        const lblW = 240;
        const lblH = 400;
        const lblX = (1200 - lblW) / 2;
        const lblY = botY + 365;

        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,0.2)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetY = 3;
        ctx.drawImage(lbl, lblX, lblY, lblW, lblH);
        ctx.restore();

        ctx.save();
        const cylGrad = ctx.createLinearGradient(lblX, lblY, lblX + lblW, lblY);
        cylGrad.addColorStop(0, 'rgba(0,0,0,0.18)');
        cylGrad.addColorStop(0.1, 'transparent');
        cylGrad.addColorStop(0.9, 'transparent');
        cylGrad.addColorStop(1, 'rgba(0,0,0,0.18)');
        ctx.fillStyle = cylGrad;
        ctx.fillRect(lblX, lblY, lblW, lblH);
        ctx.restore();
      }

      return canvas.toDataURL('image/png');
    }

    // ── 3. HOME SPRAY ORIGINAL (ENVASE ÁMBAR / CAFÉ) ──────────────
    async function drawHomeSprayOriginal(imgBotSrc, imgLblSrc) {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1200, 1200);

      const botRaw = await loadImage(imgBotSrc);
      const lbl = await loadImage(imgLblSrc);

      const botW = 540;
      const botH = 900;
      const botX = (1200 - botW) / 2;
      const botY = 160;

      const botClean = makeBackgroundTransparent(botRaw, botW, botH, 235);

      ctx.save();
      ctx.beginPath();
      ctx.ellipse(600, 1045, 170, 22, 0, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.15)';
      ctx.filter = 'blur(14px)';
      ctx.fill();
      ctx.restore();

      ctx.drawImage(botClean, botX, botY);

      if (lbl) {
        const lblW = 168;
        const lblH = 210;
        const lblX = (1200 - lblW) / 2;
        const lblY = botY + 440;

        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,0.25)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetY = 3;
        ctx.drawImage(lbl, lblX, lblY, lblW, lblH);
        ctx.restore();

        ctx.save();
        const cylGrad = ctx.createLinearGradient(lblX, lblY, lblX + lblW, lblY);
        cylGrad.addColorStop(0, 'rgba(0,0,0,0.2)');
        cylGrad.addColorStop(0.12, 'transparent');
        cylGrad.addColorStop(0.88, 'transparent');
        cylGrad.addColorStop(1, 'rgba(0,0,0,0.2)');
        ctx.fillStyle = cylGrad;
        ctx.fillRect(lblX, lblY, lblW, lblH);
        ctx.restore();
      }

      return canvas.toDataURL('image/png');
    }

    // ── 4. HOME SPRAY TRANSPARENTE CON LÍQUIDO CAFÉ CLARO ──────────
    async function drawHomeSprayTransparente(imgBotSrc, imgLblSrc) {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1200, 1200);

      const botRaw = await loadImage(imgBotSrc);
      const lbl = await loadImage(imgLblSrc);

      const botW = 540;
      const botH = 900;
      const botX = (1200 - botW) / 2;
      const botY = 160;

      const botClean = makeBackgroundTransparent(botRaw, botW, botH, 235);
      const bCtx = botClean.getContext('2d');
      const imgData = bCtx.getImageData(0, 0, botW, botH);
      const d = imgData.data;

      // Transformación de cuerpo ámbar a vidrio transparente con líquido café claro
      for (let i = 0; i < d.length; i += 4) {
        if (d[i+3] > 0) {
          const r = d[i], g = d[i+1], b = d[i+2];
          if (r < 75 && g < 75 && b < 75) {
            // Boquilla negra intacta
          } else {
            // Vidrio claro con líquido café ámbar luminoso (#CFA06B)
            const lum = (r * 0.3 + g * 0.59 + b * 0.11) / 255;
            d[i]   = Math.min(255, Math.floor(215 * lum + 30));
            d[i+1] = Math.min(255, Math.floor(165 * lum + 20));
            d[i+2] = Math.min(255, Math.floor(105 * lum + 10));
          }
        }
      }
      bCtx.putImageData(imgData, 0, 0);

      // Tubo de aspiración visible en el interior de la botella (debajo de la rosca)
      bCtx.save();
      bCtx.beginPath();
      bCtx.moveTo(botW / 2 - 2, 270);
      bCtx.bezierCurveTo(botW / 2 - 8, 450, botW / 2 - 22, 650, botW / 2 - 30, 840);
      bCtx.lineWidth = 5;
      bCtx.strokeStyle = 'rgba(255,255,255,0.85)';
      bCtx.stroke();
      bCtx.restore();

      ctx.save();
      ctx.beginPath();
      ctx.ellipse(600, 1045, 170, 22, 0, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.14)';
      ctx.filter = 'blur(14px)';
      ctx.fill();
      ctx.restore();

      ctx.drawImage(botClean, botX, botY);

      if (lbl) {
        const lblW = 168;
        const lblH = 210;
        const lblX = (1200 - lblW) / 2;
        const lblY = botY + 440;

        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,0.2)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetY = 3;
        ctx.drawImage(lbl, lblX, lblY, lblW, lblH);
        ctx.restore();

        ctx.save();
        const cylGrad = ctx.createLinearGradient(lblX, lblY, lblX + lblW, lblY);
        cylGrad.addColorStop(0, 'rgba(0,0,0,0.18)');
        cylGrad.addColorStop(0.1, 'rgba(255,255,255,0.1)');
        cylGrad.addColorStop(0.9, 'rgba(255,255,255,0.1)');
        cylGrad.addColorStop(1, 'rgba(0,0,0,0.18)');
        ctx.fillStyle = cylGrad;
        ctx.fillRect(lblX, lblY, lblW, lblH);
        ctx.restore();
      }

      return canvas.toDataURL('image/png');
    }

    // ── 5. RECARGA 250 ML ──────────────────────────────────────────
    async function drawRecarga250(imgBotSrc, imgLblSrc) {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1200, 1200);

      const botRaw = await loadImage(imgBotSrc);
      const lbl = await loadImage(imgLblSrc);

      const botW = 420;
      const botH = 920;
      const botX = (1200 - botW) / 2;
      const botY = 160;

      const botClean = makeBackgroundTransparent(botRaw, botW, botH, 235);

      ctx.save();
      ctx.beginPath();
      ctx.ellipse(600, 1065, 180, 22, 0, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.14)';
      ctx.filter = 'blur(12px)';
      ctx.fill();
      ctx.restore();

      ctx.drawImage(botClean, botX, botY);

      if (lbl) {
        const lblW = 250;
        const lblH = 315;
        const lblX = (1200 - lblW) / 2;
        const lblY = botY + 420;

        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,0.18)';
        ctx.shadowBlur = 12;
        ctx.shadowOffsetY = 4;
        ctx.drawImage(lbl, lblX, lblY, lblW, lblH);
        ctx.restore();
      }

      return canvas.toDataURL('image/png');
    }

    // ── 6. AROMATIZADOR 15 ML ──────────────────────────────────────
    async function drawAromatizador(imgBotSrc, imgLblSrc) {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1200, 1200);

      const botRaw = await loadImage(imgBotSrc);
      const lbl = await loadImage(imgLblSrc);

      const botW = 680;
      const botH = 880;
      const botX = (1200 - botW) / 2 - 20;
      const botY = 170;

      const botClean = makeBackgroundTransparent(botRaw, botW, botH, 235);

      ctx.save();
      ctx.beginPath();
      ctx.ellipse(600, 1035, 190, 24, 0, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.14)';
      ctx.filter = 'blur(14px)';
      ctx.fill();
      ctx.restore();

      ctx.drawImage(botClean, botX, botY);

      if (lbl) {
        const lblRadius = 135;
        const lblX = botX + 275;
        const lblY = botY + 455;

        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,0.22)';
        ctx.shadowBlur = 12;
        ctx.shadowOffsetY = 4;

        ctx.beginPath();
        ctx.arc(lblX + lblRadius, lblY + lblRadius, lblRadius, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(lbl, lblX, lblY, lblRadius * 2, lblRadius * 2);
        ctx.restore();

        ctx.save();
        ctx.beginPath();
        ctx.arc(lblX + lblRadius, lblY + lblRadius, lblRadius, 0, Math.PI * 2);
        const sphereGrad = ctx.createRadialGradient(
          lblX + lblRadius - 30, lblY + lblRadius - 30, 10,
          lblX + lblRadius, lblY + lblRadius, lblRadius
        );
        sphereGrad.addColorStop(0, 'rgba(255,255,255,0.25)');
        sphereGrad.addColorStop(0.6, 'transparent');
        sphereGrad.addColorStop(1, 'rgba(0,0,0,0.14)');
        ctx.fillStyle = sphereGrad;
        ctx.fill();
        ctx.restore();
      }

      return canvas.toDataURL('image/png');
    }
  </script>
</body>
</html>`;

  await page.setContent(htmlContent, { waitUntil: 'domcontentloaded' });

  async function saveCanvasResult(funcCall, filename) {
    const dataUrl = await page.evaluate(funcCall);
    const base64Data = dataUrl.replace(/^data:image\/png;base64,/, '');
    const outPath = path.join(outDir, filename);
    fs.writeFileSync(outPath, Buffer.from(base64Data, 'base64'));
    console.log(`  ✅ Generado: ${filename}`);
  }

  await saveCanvasResult(`drawMikado('${imgMikado}', '${labelMikado}')`, 'Montaje_Mikado_Vainilla_Coco.png');
  await saveCanvasResult(`drawRecarga500('${imgRecarga500}', '${labelRecarga500}')`, 'Montaje_Recarga_500ml_Lavanda.png');
  await saveCanvasResult(`drawHomeSprayOriginal('${imgHomeSprayOrig}', '${labelHomeSprayCafe}')`, 'Montaje_Home_Spray_Original_Coco_Flower.png');
  await saveCanvasResult(`drawHomeSprayTransparente('${imgHomeSprayOrig}', '${labelHomeSprayTransp}')`, 'Montaje_Home_Spray_Transparente_Manzana_Canela.png');
  await saveCanvasResult(`drawRecarga250('${imgRecarga250}', '${labelRecarga250}')`, 'Montaje_Recarga_250ml_Berries.png');
  await saveCanvasResult(`drawAromatizador('${imgAromatizador}', '${labelAromatizador}')`, 'Montaje_Aromatizador_Coco_Nut.png');

  await browser.close();
  console.log(`\n🎉 ¡Todos los montajes completados exitosamente!`);
}

renderMontages().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
