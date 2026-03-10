const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const config = require('./config.json');

// Import vendor handlers
const handlers = {
  'OnPress': require('./vendor_handlers/onpress'),
  '48 Hour Books': require('./vendor_handlers/48hrbooks'),
  'Mixam': require('./vendor_handlers/mixam'),
  'BookBaby': require('./vendor_handlers/bookbaby'),
  'Books.by': require('./vendor_handlers/booksby'),
  'Lightning Press': require('./vendor_handlers/lightningpress'),
  'Gorham Printing': require('./vendor_handlers/gorhamprinting'),
  'DiggyPOD': require('./vendor_handlers/diggypod'),
  'Doxzoo': require('./vendor_handlers/doxzoo'),
  'The Book Patch': require('./vendor_handlers/thebookpatch'),
  'Gatekeeper Press': require('./vendor_handlers/gatekeeperpress'),
  'Greenerprinter': require('./vendor_handlers/greenerprinter'),
  'MCRL Printing': require('./vendor_handlers/mcrlprinting'),
  'PRC Book Printing': require('./vendor_handlers/prcbookprinting'),
  'PrintIndustry': require('./vendor_handlers/printindustry'),
  'World Publishing Company': require('./vendor_handlers/worldpublishing'),
};

function makeEmptyResult(vendor, quantity) {
  return {
    vendor_name: vendor.name,
    vendor_url: vendor.url,
    date_checked: new Date().toISOString().split('T')[0],
    instant_quote_available: 'no',
    product_type_used: '',
    trim_size_used: '',
    page_count_used: '',
    binding_used: '',
    interior_color: '',
    interior_stock_name: '',
    interior_stock_finish: '',
    gloss_available_for_hardcover: 'unclear',
    quantity: quantity,
    print_price: '',
    shipping_price: '',
    total_price: '',
    turnaround_time: '',
    notes: '',
    quote_url: '',
    screenshot_path: '',
    status: 'pending',
  };
}

function resultsToCsv(results) {
  if (results.length === 0) return '';
  const headers = Object.keys(results[0]);
  const lines = [headers.join(',')];
  for (const row of results) {
    const vals = headers.map(h => {
      const v = String(row[h] ?? '');
      // Escape CSV fields containing commas, quotes, or newlines
      if (v.includes(',') || v.includes('"') || v.includes('\n')) {
        return '"' + v.replace(/"/g, '""') + '"';
      }
      return v;
    });
    lines.push(vals.join(','));
  }
  return lines.join('\n') + '\n';
}

function generateMarkdownSummary(results) {
  const lines = [];
  lines.push('# Printing Quote Comparison');
  lines.push('');
  lines.push(`**Date:** ${new Date().toISOString().split('T')[0]}`);
  lines.push(`**Product:** ${config.book_specs.product}`);
  lines.push(`**Trim:** ${config.book_specs.trim_size} ${config.book_specs.orientation}`);
  lines.push(`**Binding:** ${config.book_specs.binding}`);
  lines.push(`**Pages:** ${config.book_specs.page_count}`);
  lines.push(`**Interior:** ${config.book_specs.interior_color}, ${config.book_specs.interior_stock}`);
  lines.push(`**Quantities:** ${config.quantities.join(', ')}`);
  lines.push(`**Ship to:** ${config.shipping.zip_code}`);
  lines.push('');

  // Successful quotes
  const successful = results.filter(r => r.status === 'success' || r.status === 'partial');
  const rejected = results.filter(r => r.status === 'rejected_non_gloss');
  const blocked = results.filter(r => r.status === 'blocked' || r.status === 'manual_follow_up_needed');

  for (const qty of config.quantities) {
    lines.push(`## Quotes for Quantity: ${qty}`);
    lines.push('');
    const qtyResults = successful.filter(r => r.quantity === qty);
    if (qtyResults.length === 0) {
      lines.push('_No successful quotes for this quantity._');
    } else {
      lines.push('| Vendor | Print Price | Shipping | Total | Turnaround | Stock Used | Status |');
      lines.push('|--------|------------|----------|-------|------------|------------|--------|');
      // Sort by total_price if numeric
      qtyResults.sort((a, b) => {
        const pa = parseFloat(String(a.total_price || a.print_price).replace(/[$,]/g, '')) || 999999;
        const pb = parseFloat(String(b.total_price || b.print_price).replace(/[$,]/g, '')) || 999999;
        return pa - pb;
      });
      for (const r of qtyResults) {
        lines.push(`| ${r.vendor_name} | ${r.print_price || 'N/A'} | ${r.shipping_price || 'N/A'} | ${r.total_price || 'N/A'} | ${r.turnaround_time || 'N/A'} | ${r.interior_stock_name || 'N/A'} | ${r.status} |`);
      }
    }
    lines.push('');
  }

  if (rejected.length > 0) {
    lines.push('## Rejected Vendors (No Glossy Hardcover Interior)');
    lines.push('');
    const seen = new Set();
    for (const r of rejected) {
      if (!seen.has(r.vendor_name)) {
        seen.add(r.vendor_name);
        lines.push(`- **${r.vendor_name}**: ${r.notes}`);
      }
    }
    lines.push('');
  }

  if (blocked.length > 0) {
    lines.push('## Vendors Needing Manual Follow-up');
    lines.push('');
    const seen = new Set();
    for (const r of blocked) {
      if (!seen.has(r.vendor_name)) {
        seen.add(r.vendor_name);
        lines.push(`- **${r.vendor_name}** (${r.status}): ${r.notes}`);
        if (r.quote_url) lines.push(`  - Quote URL: ${r.quote_url}`);
      }
    }
    lines.push('');
  }

  lines.push('## Caveats');
  lines.push('');
  lines.push('- Paper stock names vary by vendor. "Closest equivalent" flags indicate the vendor does not offer an exact 100# gloss text match.');
  lines.push('- Shipping prices may vary based on method selected.');
  lines.push('- Prices are point-in-time snapshots and may change.');
  lines.push('');

  return lines.join('\n');
}

function printConsoleRanking(results) {
  console.log('\n' + '='.repeat(80));
  console.log('QUOTE COMPARISON RANKING');
  console.log('='.repeat(80));

  const successful = results.filter(r => r.status === 'success' || r.status === 'partial');
  const rejected = results.filter(r => r.status === 'rejected_non_gloss');

  for (const qty of config.quantities) {
    console.log(`\n--- Quantity: ${qty} (sorted by lowest total delivered price) ---`);
    const qtyResults = successful.filter(r => r.quantity === qty);
    if (qtyResults.length === 0) {
      console.log('  No successful quotes.');
      continue;
    }
    qtyResults.sort((a, b) => {
      const pa = parseFloat(String(a.total_price || a.print_price).replace(/[$,]/g, '')) || 999999;
      const pb = parseFloat(String(b.total_price || b.print_price).replace(/[$,]/g, '')) || 999999;
      return pa - pb;
    });
    for (let i = 0; i < qtyResults.length; i++) {
      const r = qtyResults[i];
      const price = r.total_price || r.print_price || 'N/A';
      const stock = r.interior_stock_name || 'unknown';
      console.log(`  ${i + 1}. ${r.vendor_name.padEnd(20)} ${String(price).padEnd(12)} stock: ${stock}  [${r.status}]`);
    }
  }

  if (rejected.length > 0) {
    console.log('\n--- REJECTED (no glossy hardcover interior) ---');
    const seen = new Set();
    for (const r of rejected) {
      if (!seen.has(r.vendor_name)) {
        seen.add(r.vendor_name);
        console.log(`  X  ${r.vendor_name}: ${r.notes}`);
      }
    }
  }

  const followUp = results.filter(r => r.status === 'blocked' || r.status === 'manual_follow_up_needed');
  if (followUp.length > 0) {
    console.log('\n--- NEEDS MANUAL FOLLOW-UP ---');
    const seen = new Set();
    for (const r of followUp) {
      if (!seen.has(r.vendor_name)) {
        seen.add(r.vendor_name);
        console.log(`  ?  ${r.vendor_name}: ${r.notes}`);
      }
    }
  }

  console.log('\n' + '='.repeat(80));
}

async function main() {
  const screenshotDir = path.join(__dirname, config.output.screenshot_dir);
  fs.mkdirSync(screenshotDir, { recursive: true });

  const browser = await chromium.launch({
    headless: config.browser.headless,
  });

  const allResults = [];

  for (const vendor of config.vendors) {
    if (!vendor.enabled) {
      console.log(`Skipping disabled vendor: ${vendor.name}`);
      continue;
    }

    const handler = handlers[vendor.name];
    if (!handler) {
      console.log(`No handler for vendor: ${vendor.name}`);
      for (const qty of config.quantities) {
        const r = makeEmptyResult(vendor, qty);
        r.status = 'manual_follow_up_needed';
        r.notes = 'No automated handler implemented yet';
        allResults.push(r);
      }
      continue;
    }

    console.log(`\n${'─'.repeat(60)}`);
    console.log(`Processing: ${vendor.name}`);
    console.log(`${'─'.repeat(60)}`);

    const context = await browser.newContext({
      viewport: { width: 1280, height: 900 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    });
    const page = await context.newPage();

    try {
      for (const qty of config.quantities) {
        console.log(`  Quantity: ${qty}`);
        const result = makeEmptyResult(vendor, qty);
        try {
          const quoteData = await handler.getQuote(page, config, qty, screenshotDir);
          Object.assign(result, quoteData);
          result.quantity = qty;
          result.vendor_name = vendor.name;
          result.vendor_url = vendor.url;
          result.date_checked = new Date().toISOString().split('T')[0];
          console.log(`    Status: ${result.status} | Price: ${result.print_price || 'N/A'}`);
        } catch (err) {
          result.status = 'blocked';
          result.notes = `Error: ${err.message}`;
          const ssPath = path.join(screenshotDir, `${vendor.name.replace(/\s+/g, '_')}_error_q${qty}.png`);
          try { await page.screenshot({ path: ssPath, fullPage: true }); result.screenshot_path = ssPath; } catch (_) {}
          console.log(`    ERROR: ${err.message}`);
        }
        allResults.push(result);
      }
    } finally {
      await context.close();
    }
  }

  await browser.close();

  // Write CSV
  const csvPath = path.join(__dirname, config.output.csv_path);
  fs.writeFileSync(csvPath, resultsToCsv(allResults));
  console.log(`\nCSV written to: ${csvPath}`);

  // Write markdown summary
  const mdPath = path.join(__dirname, config.output.markdown_path);
  fs.writeFileSync(mdPath, generateMarkdownSummary(allResults));
  console.log(`Markdown written to: ${mdPath}`);

  // Console ranking
  printConsoleRanking(allResults);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
