/**
 * render_pdf.js - HTML to PDF Renderer
 * 
 * Converts HTML files to PDF using Chromium/Chrome browser engine
 * 
 * Usage:
 *   node render_pdf.js input.html output.pdf
 * 
 * Requirements:
 *   npm install puppeteer
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

/**
 * Convert HTML file to PDF
 * @param {string} htmlPath - Path to input HTML file
 * @param {string} pdfPath - Path to output PDF file
 * @param {object} options - PDF options (pageSize, margin, etc.)
 */
async function htmlToPdf(htmlPath, pdfPath, options = {}) {
    let browser;
    
    try {
        // Validate input file exists
        if (!fs.existsSync(htmlPath)) {
            throw new Error(`Input file not found: ${htmlPath}`);
        }
        
        // Default options
        const defaultOptions = {
            format: 'A4',
            margin: {
                top: '10mm',
                bottom: '10mm',
                left: '10mm',
                right: '10mm'
            },
            printBackground: true,
            preferCSSPageSize: true
        };
        
        const pdfOptions = { ...defaultOptions, ...options };
        
        // Launch browser
        browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        // Open page
        const page = await browser.newPage();
        
        // Load HTML file
        const htmlUrl = `file://${path.resolve(htmlPath)}`;
        await page.goto(htmlUrl, { waitUntil: 'networkidle2' });
        
        // Generate PDF
        await page.pdf({
            path: pdfPath,
            ...pdfOptions
        });
        
        console.log(`✓ PDF generated: ${pdfPath}`);
        return true;
        
    } catch (error) {
        console.error(`✗ Error: ${error.message}`);
        return false;
        
    } finally {
        // Close browser
        if (browser) {
            await browser.close();
        }
    }
}

/**
 * Convert multiple HTML files to PDF
 * @param {array} files - Array of {input, output} objects
 */
async function batchConvert(files) {
    console.log(`Converting ${files.length} files to PDF...`);
    
    for (const file of files) {
        await htmlToPdf(file.input, file.output);
    }
    
    console.log('Batch conversion complete!');
}

// Command line usage
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.log(`
Usage:
  node render_pdf.js <input.html> <output.pdf>

Example:
  node render_pdf.js report.html report.pdf
  node render_pdf.js schematic.html schematic.pdf

Requirements:
  npm install puppeteer
        `);
        process.exit(1);
    }
    
    const inputFile = args[0];
    const outputFile = args[1];
    
    htmlToPdf(inputFile, outputFile).then(success => {
        process.exit(success ? 0 : 1);
    });
}

module.exports = { htmlToPdf, batchConvert };
