// render_pdf.js — render an HTML (with inline SVG) file to a Letter PDF via Chromium.
// Usage: node render_pdf.js <input.html> <output.pdf>
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const [, , inPath, outPath] = process.argv;
  if (!inPath || !outPath) {
    console.error('Usage: node render_pdf.js <input.html> <output.pdf>');
    process.exit(1);
  }
  const html = fs.readFileSync(inPath, 'utf8');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.pdf({
    path: outPath,
    format: 'Letter',
    printBackground: true,
    margin: { top: '14mm', bottom: '12mm', left: '14mm', right: '14mm' },
  });
  await browser.close();
  console.log('wrote', outPath);
})();
