/**
 * 48 Hour Books vendor handler
 * URL: https://www.48hrbooks.com/book-printing/pricing-calculator
 * Type: Online pricing calculator
 *
 * 48 Hour Books has a pricing calculator with case binding (hardcover).
 * They offer full-color printing and various paper stocks.
 */

const path = require('path');

async function getQuote(page, config, quantity, screenshotDir) {
  const specs = config.book_specs;
  const result = {
    instant_quote_available: 'yes',
    product_type_used: 'Book Printing',
    status: 'pending',
  };

  // Navigate to pricing calculator
  await page.goto('https://www.48hrbooks.com/book-printing/pricing-calculator', {
    waitUntil: 'networkidle',
    timeout: config.browser.timeout_ms,
  });

  await page.waitForTimeout(3000);

  // Take initial screenshot
  const ssInitial = path.join(screenshotDir, `48HrBooks_initial_q${quantity}.png`);
  await page.screenshot({ path: ssInitial, fullPage: false });

  try {
    // --- Binding type: Case Binding (hardcover) ---
    const bindingSelectors = [
      'text=Case Binding',
      'text=Hardcover',
      'text=Case Bound',
      'text=Hard Cover',
      '[value="case"]',
      '[value="hardcover"]',
      'select[name*="bind"] option[value*="case"]',
    ];

    // First try select dropdowns
    const selectEls = await page.$$('select');
    for (const sel of selectEls) {
      try {
        const options = await sel.$$('option');
        for (const opt of options) {
          const text = await opt.textContent();
          if (text && (text.toLowerCase().includes('case') || text.toLowerCase().includes('hardcover'))) {
            const val = await opt.getAttribute('value');
            await sel.selectOption(val);
            await page.waitForTimeout(1000);
            result.binding_used = text.trim();
            break;
          }
        }
        if (result.binding_used) break;
      } catch (_) {}
    }

    // If no select worked, try clicking
    if (!result.binding_used) {
      for (const sel of bindingSelectors) {
        try {
          const el = await page.$(sel);
          if (el && await el.isVisible()) {
            await el.click();
            await page.waitForTimeout(1000);
            result.binding_used = 'Case Binding';
            break;
          }
        } catch (_) {}
      }
    }

    // --- Trim size ---
    // Try to find size selector and pick 8.5x11 or 11x8.5
    const sizeTexts = ['8.5 x 11', '8.5" x 11"', '8.5x11', '11 x 8.5', '11x8.5'];
    for (const sel of selectEls) {
      try {
        const options = await sel.$$('option');
        for (const opt of options) {
          const text = await opt.textContent();
          if (text && sizeTexts.some(s => text.includes(s))) {
            const val = await opt.getAttribute('value');
            await sel.selectOption(val);
            await page.waitForTimeout(1000);
            result.trim_size_used = text.trim();
            break;
          }
        }
        if (result.trim_size_used) break;
      } catch (_) {}
    }

    // --- Interior color ---
    const colorTexts = ['Full Color', 'Color', '4/4', 'CMYK'];
    for (const sel of selectEls) {
      try {
        const options = await sel.$$('option');
        for (const opt of options) {
          const text = await opt.textContent();
          if (text && colorTexts.some(c => text.toLowerCase().includes(c.toLowerCase()))) {
            const val = await opt.getAttribute('value');
            await sel.selectOption(val);
            await page.waitForTimeout(1000);
            result.interior_color = text.trim();
            break;
          }
        }
        if (result.interior_color && result.interior_color !== '') break;
      } catch (_) {}
    }

    // --- Paper stock - look for gloss ---
    for (const sel of selectEls) {
      try {
        const options = await sel.$$('option');
        for (const opt of options) {
          const text = await opt.textContent();
          if (text && text.toLowerCase().includes('gloss')) {
            const val = await opt.getAttribute('value');
            await sel.selectOption(val);
            await page.waitForTimeout(1000);
            result.interior_stock_name = text.trim();
            result.interior_stock_finish = 'gloss';
            result.gloss_available_for_hardcover = 'yes';
            break;
          }
        }
        if (result.interior_stock_name) break;
      } catch (_) {}
    }

    if (!result.interior_stock_name) {
      // Check if any gloss option exists at all
      const bodyText = await page.textContent('body');
      if (bodyText.toLowerCase().includes('gloss')) {
        result.gloss_available_for_hardcover = 'yes';
        result.notes = (result.notes || '') + 'Gloss option detected but could not auto-select. ';
      } else {
        result.gloss_available_for_hardcover = 'unclear';
        result.notes = (result.notes || '') + 'Could not confirm gloss paper availability. ';
      }
    }

    // --- Page count ---
    const pageInputs = await page.$$('input[type="number"], input[type="text"]');
    for (const inp of pageInputs) {
      try {
        const name = (await inp.getAttribute('name') || '').toLowerCase();
        const id = (await inp.getAttribute('id') || '').toLowerCase();
        const placeholder = (await inp.getAttribute('placeholder') || '').toLowerCase();
        if (name.includes('page') || id.includes('page') || placeholder.includes('page')) {
          await inp.fill('');
          await inp.fill(String(specs.page_count));
          await inp.press('Tab');
          await page.waitForTimeout(1000);
          result.page_count_used = String(specs.page_count);
          break;
        }
      } catch (_) {}
    }

    // --- Quantity ---
    for (const inp of pageInputs) {
      try {
        const name = (await inp.getAttribute('name') || '').toLowerCase();
        const id = (await inp.getAttribute('id') || '').toLowerCase();
        const placeholder = (await inp.getAttribute('placeholder') || '').toLowerCase();
        if (name.includes('quant') || id.includes('quant') || name.includes('qty') || placeholder.includes('quant')) {
          await inp.fill('');
          await inp.fill(String(quantity));
          await inp.press('Tab');
          await page.waitForTimeout(1500);
          break;
        }
      } catch (_) {}
    }

    // Try to submit/calculate
    const calcButtons = [
      'text=Calculate',
      'text=Get Price',
      'text=Get Quote',
      'text=Update',
      'button[type="submit"]',
      'input[type="submit"]',
    ];
    for (const sel of calcButtons) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(3000);
          break;
        }
      } catch (_) {}
    }

    await page.waitForTimeout(2000);

    // --- Extract price ---
    const bodyText = await page.textContent('body');

    // Look for price patterns
    const pricePatterns = [
      /(?:Total|Price|Cost|Subtotal)[:\s]*\$([\d,.]+)/i,
      /\$([\d,.]+)\s*(?:total|per\s*book|each)/i,
      /printing\s*(?:cost|price)?[:\s]*\$([\d,.]+)/i,
    ];

    for (const pat of pricePatterns) {
      const m = bodyText.match(pat);
      if (m) {
        result.print_price = '$' + m[1];
        result.total_price = '$' + m[1];
        result.status = 'success';
        break;
      }
    }

    // Look for per-unit price too
    const perUnitMatch = bodyText.match(/\$([\d.]+)\s*(?:per\s*(?:book|copy|unit)|each)/i);
    if (perUnitMatch) {
      result.notes = (result.notes || '') + `Per-unit price: $${perUnitMatch[1]}. `;
    }

    // Look for turnaround
    const turnaroundMatch = bodyText.match(/(\d+)\s*(?:business\s*)?day/i);
    if (turnaroundMatch) {
      result.turnaround_time = turnaroundMatch[0];
    }

    // Final screenshot
    const ssFinal = path.join(screenshotDir, `48HrBooks_quote_q${quantity}.png`);
    await page.screenshot({ path: ssFinal, fullPage: false });
    result.screenshot_path = ssFinal;

    if (result.status !== 'success') {
      result.status = 'partial';
      result.notes = (result.notes || '') + 'Calculator loaded but price extraction incomplete. Visit the calculator manually. ';
      result.quote_url = 'https://www.48hrbooks.com/book-printing/pricing-calculator';
    }

  } catch (err) {
    result.status = 'blocked';
    result.notes = `Automation error: ${err.message}`;
    const ssErr = path.join(screenshotDir, `48HrBooks_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssErr, fullPage: true }); result.screenshot_path = ssErr; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
