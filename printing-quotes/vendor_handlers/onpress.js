/**
 * OnPress Book Printing vendor handler
 * URL: https://www.onpressbookprinting.com/Quoter/Default.aspx
 * Type: Online quoter (ASP.NET web form)
 *
 * OnPress uses an ASP.NET-based quoter with postback-driven form updates.
 * Fields include trim size, binding, paper stock, page count, quantity, etc.
 */

const path = require('path');

async function getQuote(page, config, quantity, screenshotDir) {
  const specs = config.book_specs;
  const result = {
    instant_quote_available: 'yes',
    product_type_used: 'Book Printing',
    status: 'pending',
  };

  // Navigate to the OnPress quoter
  await page.goto('https://www.onpressbookprinting.com/Quoter/Default.aspx', {
    waitUntil: 'networkidle',
    timeout: config.browser.timeout_ms,
  });

  await page.waitForTimeout(3000);

  const ssInitial = path.join(screenshotDir, `OnPress_initial_q${quantity}.png`);
  await page.screenshot({ path: ssInitial, fullPage: false });

  try {
    // Collect all select elements and inputs for analysis
    const selectEls = await page.$$('select');
    const inputEls = await page.$$('input');

    // Map selects by their label or id/name for easier targeting
    const selectMap = {};
    for (const sel of selectEls) {
      const id = await sel.getAttribute('id') || '';
      const name = await sel.getAttribute('name') || '';
      const options = await sel.$$eval('option', opts =>
        opts.map(o => ({ value: o.value, text: o.textContent.trim() }))
      );
      selectMap[id || name] = { element: sel, id, name, options };
    }

    // Log what we found for debugging
    const fieldInfo = Object.entries(selectMap).map(([k, v]) =>
      `${k}: [${v.options.map(o => o.text).join(', ')}]`
    );
    result.notes = (result.notes || '') + `Found ${selectEls.length} selects, ${inputEls.length} inputs. `;

    // --- Try to select binding: Hardcover / Case Bound ---
    for (const [key, info] of Object.entries(selectMap)) {
      const hasBinding = info.options.some(o =>
        /case|hard/i.test(o.text)
      );
      if (hasBinding || /bind/i.test(key)) {
        const bindOpt = info.options.find(o => /case|hard/i.test(o.text));
        if (bindOpt) {
          await info.element.selectOption(bindOpt.value);
          await page.waitForTimeout(2000); // ASP.NET postback
          result.binding_used = bindOpt.text;
        }
        break;
      }
    }

    // Re-fetch selects after postback
    const selectEls2 = await page.$$('select');
    const selectMap2 = {};
    for (const sel of selectEls2) {
      const id = await sel.getAttribute('id') || '';
      const name = await sel.getAttribute('name') || '';
      const options = await sel.$$eval('option', opts =>
        opts.map(o => ({ value: o.value, text: o.textContent.trim() }))
      );
      selectMap2[id || name] = { element: sel, id, name, options };
    }

    // --- Try to select trim size ---
    for (const [key, info] of Object.entries(selectMap2)) {
      const sizeMatch = info.options.find(o =>
        /8\.5.*11|11.*8\.5/i.test(o.text)
      );
      if (sizeMatch || /size|trim/i.test(key)) {
        const opt = sizeMatch || info.options.find(o =>
          /8\.5|11/i.test(o.text)
        );
        if (opt) {
          await info.element.selectOption(opt.value);
          await page.waitForTimeout(2000);
          result.trim_size_used = opt.text;
        }
        break;
      }
    }

    // Re-fetch after postback
    const selectEls3 = await page.$$('select');
    const selectMap3 = {};
    for (const sel of selectEls3) {
      const id = await sel.getAttribute('id') || '';
      const name = await sel.getAttribute('name') || '';
      const options = await sel.$$eval('option', opts =>
        opts.map(o => ({ value: o.value, text: o.textContent.trim() }))
      );
      selectMap3[id || name] = { element: sel, id, name, options };
    }

    // --- Interior color: Full Color ---
    for (const [key, info] of Object.entries(selectMap3)) {
      const colorOpt = info.options.find(o =>
        /full\s*color|color|4\/4|cmyk/i.test(o.text)
      );
      if (colorOpt && (/color|interior|ink/i.test(key) || colorOpt)) {
        await info.element.selectOption(colorOpt.value);
        await page.waitForTimeout(2000);
        result.interior_color = colorOpt.text;
        break;
      }
    }

    // Re-fetch after postback
    const selectEls4 = await page.$$('select');
    const selectMap4 = {};
    for (const sel of selectEls4) {
      const id = await sel.getAttribute('id') || '';
      const name = await sel.getAttribute('name') || '';
      const options = await sel.$$eval('option', opts =>
        opts.map(o => ({ value: o.value, text: o.textContent.trim() }))
      );
      selectMap4[id || name] = { element: sel, id, name, options };
    }

    // --- Paper stock: gloss ---
    for (const [key, info] of Object.entries(selectMap4)) {
      const glossOpt = info.options.find(o =>
        /gloss/i.test(o.text) && !/matte/i.test(o.text)
      );
      if (glossOpt && (/paper|stock|text\s*weight/i.test(key) || glossOpt)) {
        await info.element.selectOption(glossOpt.value);
        await page.waitForTimeout(2000);
        result.interior_stock_name = glossOpt.text;
        result.interior_stock_finish = 'gloss';
        result.gloss_available_for_hardcover = 'yes';
        break;
      }
    }

    if (!result.interior_stock_name) {
      // Check all options for any gloss mention
      let anyGloss = false;
      for (const [, info] of Object.entries(selectMap4)) {
        if (info.options.some(o => /gloss/i.test(o.text))) {
          anyGloss = true;
          break;
        }
      }
      result.gloss_available_for_hardcover = anyGloss ? 'yes' : 'unclear';
      if (!anyGloss) {
        result.notes = (result.notes || '') + 'No gloss paper option found in available dropdowns. ';
      }
    }

    // --- Page count ---
    const allInputs = await page.$$('input');
    for (const inp of allInputs) {
      const id = (await inp.getAttribute('id') || '').toLowerCase();
      const name = (await inp.getAttribute('name') || '').toLowerCase();
      if (id.includes('page') || name.includes('page')) {
        await inp.fill('');
        await inp.fill(String(specs.page_count));
        await inp.press('Tab');
        await page.waitForTimeout(2000);
        result.page_count_used = String(specs.page_count);
        break;
      }
    }

    // --- Quantity ---
    for (const inp of allInputs) {
      const id = (await inp.getAttribute('id') || '').toLowerCase();
      const name = (await inp.getAttribute('name') || '').toLowerCase();
      if (id.includes('quant') || id.includes('qty') || name.includes('quant') || name.includes('qty')) {
        await inp.fill('');
        await inp.fill(String(quantity));
        await inp.press('Tab');
        await page.waitForTimeout(2000);
        break;
      }
    }

    // Try to click Calculate/Quote button
    const calcButtonSelectors = [
      'input[value*="Calculate"]',
      'input[value*="Quote"]',
      'input[value*="Price"]',
      'input[value*="Submit"]',
      'button:has-text("Calculate")',
      'button:has-text("Quote")',
      'button:has-text("Get Price")',
      'a:has-text("Calculate")',
      '#btnQuote',
      '#btnCalc',
      '#btnSubmit',
    ];

    for (const sel of calcButtonSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(4000);
          break;
        }
      } catch (_) {}
    }

    // --- Extract price ---
    const bodyText = await page.textContent('body');

    const pricePatterns = [
      /(?:Total|Price|Cost|Subtotal|Quote)[:\s]*\$([\d,.]+)/i,
      /\$([\d,.]+)\s*(?:total|per\s*book|each)/i,
      /(?:your\s*)?(?:quote|price|cost)[:\s]*\$([\d,.]+)/gi,
    ];

    for (const pat of pricePatterns) {
      const m = bodyText.match(pat);
      if (m) {
        const priceVal = m[1] || m[0].match(/\$([\d,.]+)/)?.[1];
        if (priceVal) {
          result.print_price = '$' + priceVal;
          result.total_price = '$' + priceVal;
          result.status = 'success';
          break;
        }
      }
    }

    // Look for shipping
    const shipMatch = bodyText.match(/shipping[:\s]*\$([\d,.]+)/i);
    if (shipMatch) {
      result.shipping_price = '$' + shipMatch[1];
    }

    // Look for turnaround
    const turnMatch = bodyText.match(/(\d+)\s*(?:business\s*)?day/i);
    if (turnMatch) {
      result.turnaround_time = turnMatch[0];
    }

    // Look for per-unit cost
    const perUnitMatch = bodyText.match(/\$([\d.]+)\s*(?:per\s*(?:book|copy|unit)|each|\/\s*book)/i);
    if (perUnitMatch) {
      result.notes = (result.notes || '') + `Per-unit: $${perUnitMatch[1]}. `;
    }

    // Final screenshot
    const ssFinal = path.join(screenshotDir, `OnPress_quote_q${quantity}.png`);
    await page.screenshot({ path: ssFinal, fullPage: false });
    result.screenshot_path = ssFinal;
    result.quote_url = page.url();

    if (result.status !== 'success') {
      result.status = 'partial';
      result.notes = (result.notes || '') + 'Quoter loaded but could not fully extract price. Visit manually. ';
      result.quote_url = 'https://www.onpressbookprinting.com/Quoter/Default.aspx';
    }

  } catch (err) {
    result.status = 'blocked';
    result.notes = `Automation error: ${err.message}`;
    const ssErr = path.join(screenshotDir, `OnPress_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssErr, fullPage: true }); result.screenshot_path = ssErr; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
