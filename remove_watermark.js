const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const dir = 'E:\\Logo Jeshia\\etiquetas_impresion\\00_Montajes_Productos';
const debugDir = 'E:\\Logo Jeshia\\etiquetas_impresion\\00_Montajes_Productos\\debug';
if (!fs.existsSync(debugDir)) fs.mkdirSync(debugDir, { recursive: true });

async function removeWatermarks() {
  console.log('🧼 Removiendo marcas de agua de montajes de productos...\n');

  const browser = await puppeteer.launch({ executablePath: EDGE_PATH, headless: true, protocolTimeout: 120000 });
  const page = await browser.newPage();

  const files = ['montaje_aromatizador.png', 'montaje_home_spray.png', 'montaje_mikado.png', 'montaje_recarga_250.png', 'montaje_recarga_500.png', 'm_mikado_blanco.png'];

  for (const file of files) {
    const filePath = path.join(dir, file);
    if (!fs.existsSync(filePath)) continue;

    const b64 = `data:image/png;base64,${fs.readFileSync(filePath).toString('base64')}`;

    const result = await page.evaluate(async (src) => {
      const img = new Image();
      await new Promise(r => { img.onload = r; img.src = src; });

      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);

      const w = img.width;
      const h = img.height;
      const imgData = ctx.getImageData(0, 0, w, h);
      const data = imgData.data;

      // Check corner background brightness
      let cornerSum = 0;
      for (let y = h - 50; y < h; y++) {
        for (let x = w - 50; x < w; x++) {
          const idx = (y * w + x) * 4;
          cornerSum += (data[idx] + data[idx+1] + data[idx+2]) / 3;
        }
      }
      const avgCorner = cornerSum / (50 * 50);

      if (avgCorner > 240) {
        // Pure white background montages
        for (let y = h - 300; y < h; y++) {
          for (let x = w - 300; x < w; x++) {
            const idx = (y * w + x) * 4;
            if (data[idx] > 200 && data[idx+1] > 200 && data[idx+2] > 200) {
              data[idx]   = 255;
              data[idx+1] = 255;
              data[idx+2] = 255;
              data[idx+3] = 255;
            }
          }
        }
      } else {
        // Wood texture background: inpaint ONLY the star mask area
        const starCenterX = Math.round(w - 110);
        const starCenterY = Math.round(h - 110);
        const starRadius = 60;

        const isMask = (x, y) => {
          const dx = x - starCenterX;
          const dy = y - starCenterY;
          const dist = Math.pow(Math.pow(Math.abs(dx), 0.7) + Math.pow(Math.abs(dy), 0.7), 1 / 0.7);
          return dist <= starRadius;
        };

        const newData = new Uint8ClampedArray(data);

        for (let y = starCenterY - starRadius - 5; y <= starCenterY + starRadius + 5; y++) {
          for (let x = starCenterX - starRadius - 5; x <= starCenterX + starRadius + 5; x++) {
            if (x < 0 || x >= w || y < 0 || y >= h) continue;

            if (isMask(x, y)) {
              const srcX = x - 95;
              const idx = (y * w + x) * 4;
              const sIdx = (y * w + srcX) * 4;

              newData[idx]   = data[sIdx];
              newData[idx+1] = data[sIdx+1];
              newData[idx+2] = data[sIdx+2];
            }
          }
        }

        // Feather boundary
        for (let y = starCenterY - starRadius - 6; y <= starCenterY + starRadius + 6; y++) {
          for (let x = starCenterX - starRadius - 6; x <= starCenterX + starRadius + 6; x++) {
            if (x < 1 || x >= w - 1 || y < 1 || y >= h - 1) continue;

            const dx = x - starCenterX, dy = y - starCenterY;
            const dist = Math.pow(Math.pow(Math.abs(dx), 0.7) + Math.pow(Math.abs(dy), 0.7), 1 / 0.7);

            if (dist >= starRadius - 4 && dist <= starRadius + 4) {
              const idx = (y * w + x) * 4;
              let sr = 0, sg = 0, sb = 0, sc = 0;

              for (let kx = -1; kx <= 1; kx++) {
                for (let ky = -1; ky <= 1; ky++) {
                  const nIdx = ((y + ky) * w + (x + kx)) * 4;
                  const weight = (kx === 0 && ky === 0) ? 3 : 1;
                  sr += newData[nIdx] * weight;
                  sg += newData[nIdx+1] * weight;
                  sb += newData[nIdx+2] * weight;
                  sc += weight;
                }
              }

              newData[idx]   = Math.round(sr / sc);
              newData[idx+1] = Math.round(sg / sc);
              newData[idx+2] = Math.round(sb / sc);
            }
          }
        }

        imgData.data.set(newData);
      }

      ctx.putImageData(imgData, 0, 0);

      // Crop debug view
      const cropCanvas = document.createElement('canvas');
      cropCanvas.width = 350; cropCanvas.height = 350;
      const cCtx = cropCanvas.getContext('2d');
      cCtx.drawImage(canvas, w - 350, h - 350, 350, 350, 0, 0, 350, 350);

      return {
        full: canvas.toDataURL('image/png'),
        crop: cropCanvas.toDataURL('image/png')
      };
    }, b64);

    const fullData = result.full.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync(filePath, Buffer.from(fullData, 'base64'));

    const cropData = result.crop.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync(path.join(debugDir, `cleaned_corner_${file}`), Buffer.from(cropData, 'base64'));

    console.log(`✅ Marca de agua eliminada exitosamente en: ${file}`);
  }

  await browser.close();
  console.log(`\n🎉 ¡Todas las marcas de agua han sido removidas exitosamente!`);
}

removeWatermarks().catch(err => {
  console.error(err);
  process.exit(1);
});
