/**
 * BookBaby vendor handler
 * URL: https://www.bookbaby.com/pricing
 * Type: Online quoter (JS configurator)
 *
 * BookBaby has a multi-step quoter at /pricing that lets you configure
 * book specs and see instant pricing. Hardcover and various paper stocks available.
 */

const path = require('path');

async function getQuote(page, config, quantity, screenshotDir) {
  const specs = config.book_specs;
  const result = {
    instant_quote_available: 'yes',
    product_type_used: 'Book Printing',
    status: 'pending',
  };

  // Navigate to BookBaby pricing page
  await page.goto('https://www.bookbaby.com/pricing', {
    waitUntil: 'networkidle',
    timeout: config.browser.timeout_ms,
  });

  await page.waitForTimeout(4000);

  const ssInitial = path.join(screenshotDir, `BookBaby_initial_q${quantity}.png`);
  await page.screenshot({ path: ssInitial, fullPage: false });

  try {
    // BookBaby uses a step-by-step configurator
    // Typically: Book Type -> Trim Size -> Page Count -> Paper -> Binding -> Quantity

    // --- Book type: might need to select "Printed Book" or similar ---
    const bookTypeSelectors = [
      'text=Printed Book',
      'text=Print Only',
      'text=Book Printing',
      '[data-value="print"]',
    ];
    for (const sel of bookTypeSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(2000);
          break;
        }
      } catch (_) {}
    }

    // --- Binding: Hardcover ---
    const bindingSelectors = [
      'text=Hardcover',
      'text=Hard Cover',
      'text=Case Bound',
      'text=Casebound',
      '[data-value="hardcover"]',
      '[data-binding="hardcover"]',
    ];
    for (const sel of bindingSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(2000);
          result.binding_used = 'Hardcover';
          break;
        }
      } catch (_) {}
    }

    // Also try select dropdowns
    if (!result.binding_used) {
      const selectEls = await page.$$('select');
      for (const sel of selectEls) {
        const options = await sel.$$eval('option', opts =>
          opts.map(o => ({ value: o.value, text: o.textContent.trim() }))
        );
        const hcOpt = options.find(o => /hard|case/i.test(o.text));
        if (hcOpt) {
          await sel.selectOption(hcOpt.value);
          await page.waitForTimeout(2000);
          result.binding_used = hcOpt.text;
          break;
        }
      }
    }

    // --- Trim size: 8.5x11 / 11x8.5 ---
    const sizeSelectors = [
      'text=8.5" x 11"',
      'text=8.5 x 11',
      'text=11" x 8.5"',
      'text=11 x 8.5',
      '[data-value="8.5x11"]',
      '[data-value="11x8.5"]',
    ];
    for (const sel of sizeSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(2000);
          result.trim_size_used = await el.textContent();
          break;
        }
      } catch (_) {}
    }

    // Try selects for trim size
    if (!result.trim_size_used) {
      const selectEls = await page.$$('select');
      for (const sel of selectEls) {
        const options = await sel.$$eval('option', opts =>
          opts.map(o => ({ value: o.value, text: o.textContent.trim() }))
        );
        const sizeOpt = options.find(o => /8\.5.*11|11.*8\.5/i.test(o.text));
        if (sizeOpt) {
          await sel.selectOption(sizeOpt.value);
          await page.waitForTimeout(2000);
          result.trim_size_used = sizeOpt.text;
          break;
        }
      }
    }

    // --- Interior: Full Color ---
    const colorSelectors = [
      'text=Full Color',
      'text=Color',
      'text=Premium Color',
      '[data-value="color"]',
      '[data-value="fullcolor"]',
    ];
    for (const sel of colorSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(1500);
          result.interior_color = 'Full Color';
          break;
        }
      } catch (_) {}
    }

    // --- Paper stock: gloss ---
    const paperSelectors = [
      'text=Gloss',
      'text=100# Gloss',
      'text=80# Gloss',
      'text=Coated',
      'text=Premium Gloss',
      '[data-value*="gloss"]',
    ];
    for (const sel of paperSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(1500);
          const text = await el.textContent();
          result.interior_stock_name = text.trim();
          result.interior_stock_finish = 'gloss';
          result.gloss_available_for_hardcover = 'yes';
          break;
        }
      } catch (_) {}
    }

    // Try selects for paper
    if (!result.interior_stock_name) {
      const selectEls = await page.$$('select');
      for (const sel of selectEls) {
        const options = await sel.$$eval('option', opts =>
          opts.map(o => ({ value: o.value, text: o.textContent.trim() }))
        );
        const glossOpt = options.find(o => /gloss/i.test(o.text));
        if (glossOpt) {
          await sel.selectOption(glossOpt.value);
          await page.waitForTimeout(1500);
          result.interior_stock_name = glossOpt.text;
          result.interior_stock_finish = 'gloss';
          result.gloss_available_for_hardcover = 'yes';
          break;
        }
      }
    }

    if (!result.interior_stock_name) {
      result.gloss_available_for_hardcover = 'unclear';
      result.notes = (result.notes || '') + 'Could not confirm gloss paper options via automation. ';
    }

    // --- Page count ---
    const pageInputs = await page.$$('input');
    for (const inp of pageInputs) {
      const id = (await inp.getAttribute('id') || '').toLowerCase();
      const name = (await inp.getAttribute('name') || '').toLowerCase();
      const placeholder = (await inp.getAttribute('placeholder') || '').toLowerCase();
      if (id.includes('page') || name.includes('page') || placeholder.includes('page')) {
        await inp.fill('');
        await inp.fill(String(specs.page_count));
        await inp.press('Tab');
        await page.waitForTimeout(1500);
        result.page_count_used = String(specs.page_count);
        break;
      }
    }

    // --- Quantity ---
    for (const inp of pageInputs) {
      const id = (await inp.getAttribute('id') || '').toLowerCase();
      const name = (await inp.getAttribute('name') || '').toLowerCase();
      const placeholder = (await inp.getAttribute('placeholder') || '').toLowerCase();
      if (id.includes('quant') || id.includes('qty') || name.includes('quant') || name.includes('qty') || placeholder.includes('quant')) {
        await inp.fill('');
        await inp.fill(String(quantity));
        await inp.press('Tab');
        await page.waitForTimeout(2000);
        break;
      }
    }

    // Look for calculate/update button
    const calcButtons = [
      'text=Get Price',
      'text=Calculate',
      'text=Update Price',
      'text=Get Quote',
      'text=See Price',
      'button[type="submit"]',
      'input[type="submit"]',
    ];
    for (const sel of calcButtons) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(4000);
          break;
        }
      } catch (_) {}
    }

    await page.waitForTimeout(2000);

    // --- Extract price ---
    const bodyText = await page.textContent('body');

    const pricePatterns = [
      /(?:Total|Price|Cost|Subtotal)[:\s]*\$([\d,.]+)/i,
      /\$([\d,.]+)\s*(?:total|per\s*book|each)/i,
      /(?:your\s*)?(?:quote|price|cost)[:\s]*\$([\d,.]+)/gi,
      /(?:printing)[:\s]*\$([\d,.]+)/i,
    ];

    for (const pat of pricePatterns) {
      const m = bodyText.match(pat);
      if (m) {
        const priceVal = m[1];
        if (priceVal) {
          result.print_price = '$' + priceVal;
          result.total_price = '$' + priceVal;
          result.status = 'success';
          break;
        }
      }
    }

    // Shipping
    const shipMatch = bodyText.match(/shipping[:\s]*\$([\d,.]+)/i);
    if (shipMatch) {
      result.shipping_price = '$' + shipMatch[1];
    }

    // Turnaround
    const turnMatch = bodyText.match(/(\d+)\s*(?:business\s*)?day/i);
    if (turnMatch) {
      result.turnaround_time = turnMatch[0];
    }

    // Final screenshot
    const ssFinal = path.join(screenshotDir, `BookBaby_quote_q${quantity}.png`);
    await page.screenshot({ path: ssFinal, fullPage: false });
    result.screenshot_path = ssFinal;
    result.quote_url = page.url();

    if (result.status !== 'success') {
      result.status = 'partial';
      result.notes = (result.notes || '') + 'Quoter loaded but could not fully extract pricing. BookBaby uses a multi-step JS configurator that may need manual interaction. ';
      result.quote_url = 'https://www.bookbaby.com/pricing';

      // Draft follow-up text for manual use
      result.notes += `MANUAL FOLLOW-UP: Visit ${result.quote_url} and configure: Hardcover, 11"x8.5" landscape, 36 pages, full color, 100# gloss text, qty ${quantity}, ship to ${config.shipping.zip_code}. `;
    }

  } catch (err) {
    result.status = 'blocked';
    result.notes = `Automation error: ${err.message}`;
    const ssErr = path.join(screenshotDir, `BookBaby_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssErr, fullPage: true }); result.screenshot_path = ssErr; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
