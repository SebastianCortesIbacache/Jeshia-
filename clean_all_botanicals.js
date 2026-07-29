const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const dir = path.join(__dirname, 'assets', 'aromas_botanicos');

// All images that need background removal (skip vainilla_coco + citric which were done already)
const toProcess = [
  'berries', 'coco_nut', 'sugar', 'chicle',
  'manzana_canela', 'coco_flower', 'mokka',
  'limon', 'pino', 'lavanda', 'frutal_mango'
];

async function removeBg(filePath) {
  const imgBase64 = fs.readFileSync(filePath).toString('base64');
  const ext = path.extname(filePath).toLowerCase().replace('.', '');
  const mime = ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : 'image/png';
  const imgSrc = `data:${mime};base64,${imgBase64}`;

  const html = `<!DOCTYPE html><html><body>
<canvas id="c"></canvas>
<script>
const img = new Image();
img.onload = () => {
  const c = document.getElementById('c');
  c.width = img.width; c.height = img.height;
  const ctx = c.getContext('2d');
  ctx.drawImage(img, 0, 0);
  const d = ctx.getImageData(0, 0, c.width, c.height);
  const px = d.data;
  for (let i = 0; i < px.length; i += 4) {
    const r = px[i], g = px[i+1], b = px[i+2];
    // Remove any near-white/off-white/cream pixels
    if (r > 210 && g > 200 && b > 188) { px[i+3] = 0; }
  }
  ctx.putImageData(d, 0, 0);
  window.done = c.toDataURL('image/png');
};
img.src = "${imgSrc}";
</script>
</body></html>`;

  const browser = await puppeteer.launch({ executablePath: EDGE_PATH, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setContent(html);
  await page.waitForFunction('window.done !== undefined', { timeout: 30000 });
  const dataUrl = await page.evaluate(() => window.done);
  await browser.close();

  // Always save as PNG (transparent)
  const outPath = filePath.replace(/\.(jpg|jpeg)$/i, '.png');
  fs.writeFileSync(outPath, dataUrl.replace(/^data:image\/png;base64,/, ''), 'base64');
  return outPath;
}

async function main() {
  for (const name of toProcess) {
    const fp = path.join(dir, name + '.png');
    if (!fs.existsSync(fp)) { console.log(`  ⚠ Missing: ${name}.png`); continue; }
    const out = await removeBg(fp);
    console.log(`  ✓ ${name}  →  ${out}`);
  }
  console.log('\nDone — all backgrounds removed.');
}

main().catch(console.error);
