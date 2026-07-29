const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

async function removeBg(inputPath, outputPath) {
  const imgBase64 = fs.readFileSync(inputPath).toString('base64');
  const imgSrc = `data:image/png;base64,${imgBase64}`;

  const html = `<!DOCTYPE html>
<html><body>
<canvas id="c"></canvas>
<script>
const img = new Image();
img.onload = () => {
  const canvas = document.getElementById('c');
  canvas.width = img.width;
  canvas.height = img.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const data = imgData.data;
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], g = data[i+1], b = data[i+2];
    // Remove light off-white/cream background pixels
    if (r > 215 && g > 205 && b > 195) {
      data[i+3] = 0;
    }
  }
  ctx.putImageData(imgData, 0, 0);
  window.done = canvas.toDataURL('image/png');
};
img.src = "${imgSrc}";
</script>
</body></html>`;

  const browser = await puppeteer.launch({ executablePath: EDGE_PATH, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setContent(html);
  await page.waitForFunction('window.done !== undefined', { timeout: 30000 });
  const dataUrl = await page.evaluate(() => window.done);
  const base64Data = dataUrl.replace(/^data:image\/png;base64,/, '');
  fs.writeFileSync(outputPath, base64Data, 'base64');
  await browser.close();
  console.log('✓ Transparent PNG saved:', outputPath);
}

removeBg(
  path.join('e:\\Logo Jeshia', 'assets', 'aromas_botanicos', 'frutal_mango.png'),
  path.join('e:\\Logo Jeshia', 'assets', 'aromas_botanicos', 'frutal_mango.png')
).catch(console.error);
