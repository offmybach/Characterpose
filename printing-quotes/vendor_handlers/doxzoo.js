const path = require('path');

async function getQuote(page, config, quantity, screenshotDir) {
  const result = {
    instant_quote_available: 'yes',
    product_type_used: "children's book",
    trim_size_used: config.book_specs.trim_size,
    page_count_used: String(config.book_specs.page_count),
    binding_used: config.book_specs.binding,
    interior_color: config.book_specs.interior_color,
    interior_stock_name: '',
    interior_stock_finish: '',
    gloss_available_for_hardcover: 'unclear',
    print_price: '',
    shipping_price: '',
    total_price: '',
    turnaround_time: '',
    notes: '',
    quote_url: '',
    screenshot_path: '',
    status: 'pending',
  };

  try {
    await page.goto('https://doxzoo.com/en-us/documents/childrens-book-printing', {
      waitUntil: 'domcontentloaded',
      timeout: config.browser.timeout_ms,
    });
    await page.waitForTimeout(3000);

    // Look for instant quote / get started link
    const links = await page.$$('a');
    for (const link of links) {
      const text = await link.textContent().catch(() => '');
      if (/instant\s*quote|get\s*started|configure|order\s*now|start/i.test(text)) {
        await link.click();
        await page.waitForTimeout(3000);
        break;
      }
    }

    // Interact with form selects
    const allSelects = await page.$$('select');
    for (const sel of allSelects) {
      const name = await sel.getAttribute('name').catch(() => '') || '';
      const id = await sel.getAttribute('id').catch(() => '') || '';
      const label = (name + ' ' + id).toLowerCase();
      const options = await sel.$$('option');

      if (/bind|cover\s*type|book\s*type|format/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/hard\s*cover|case\s*bound|hardback/i.test(val)) {
            await sel.selectOption({ label: val.trim() });
            break;
          }
        }
        await page.waitForTimeout(2000);
      }

      if (/size|trim|dimension/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/11\s*[x×]\s*8\.?5|8\.?5\s*[x×]\s*11|a4.*landscape/i.test(val)) {
            await sel.selectOption({ label: val.trim() });
            break;
          }
        }
        await page.waitForTimeout(1500);
      }

      if (/paper|stock/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/gloss|silk|coated/i.test(val)) {
            await sel.selectOption({ label: val.trim() });
            result.interior_stock_name = val.trim();
            result.interior_stock_finish = 'gloss';
            result.gloss_available_for_hardcover = 'yes';
            break;
          }
        }
        await page.waitForTimeout(1500);
      }
    }

    // Also try clicking option buttons/cards (Doxzoo uses a configurator UI)
    const clickables = await page.$$('button, [role="button"], .option, [data-option]');
    for (const el of clickables) {
      const text = await el.textContent().catch(() => '');
      if (/hard\s*cover|case\s*bound/i.test(text)) {
        try { await el.click(); } catch (_) {}
        await page.waitForTimeout(1500);
      }
    }

    // Fill inputs
    const allInputs = await page.$$('input[type="text"], input[type="number"], input:not([type])');
    for (const inp of allInputs) {
      const name = await inp.getAttribute('name').catch(() => '') || '';
      const id = await inp.getAttribute('id').catch(() => '') || '';
      const placeholder = await inp.getAttribute('placeholder').catch(() => '') || '';
      const combined = (name + ' ' + id + ' ' + placeholder).toLowerCase();

      if (/page|pg/i.test(combined) && !/email|name|phone/i.test(combined)) {
        await inp.fill(String(config.book_specs.page_count));
      }
      if (/qty|quantity|copies/i.test(combined)) {
        await inp.fill(String(quantity));
      }
    }

    // Submit
    const buttons = await page.$$('button, input[type="submit"]');
    for (const btn of buttons) {
      const text = await btn.textContent().catch(() => '');
      if (/calculate|get.*quote|get.*price|submit|add\s*to\s*cart/i.test(text)) {
        await btn.click();
        break;
      }
    }
    await page.waitForTimeout(5000);

    const ssPath = path.join(screenshotDir, `Doxzoo_q${quantity}.png`);
    await page.screenshot({ path: ssPath, fullPage: true });
    result.screenshot_path = ssPath;

    const bodyText = await page.textContent('body').catch(() => '');

    const priceMatch = bodyText.match(/(?:total|price|cost)[:\s]*\$?([\d,]+\.?\d{0,2})/i)
      || bodyText.match(/\$([\d,]+\.?\d{0,2})/);
    if (priceMatch) {
      result.print_price = '$' + priceMatch[1];
    }

    const shipMatch = bodyText.match(/(?:shipping|delivery)[:\s]*\$?([\d,]+\.?\d{0,2})/i);
    if (shipMatch) {
      result.shipping_price = '$' + shipMatch[1];
    }

    const turnMatch = bodyText.match(/(\d+[-–]\d+\s*(?:business\s*|working\s*)?days?)/i);
    if (turnMatch) {
      result.turnaround_time = turnMatch[1];
    }

    if (result.print_price) {
      result.status = result.shipping_price ? 'success' : 'partial';
    } else {
      result.status = 'manual_follow_up_needed';
      result.notes = 'Could not extract price. Doxzoo offers instant quotes — visit site for hardcover children\'s book, 8.5x11, 36pp, full color, gloss.';
    }

    result.quote_url = page.url();
  } catch (err) {
    result.status = 'blocked';
    result.notes = `Error: ${err.message}`;
    const ssPath = path.join(screenshotDir, `Doxzoo_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssPath, fullPage: true }); result.screenshot_path = ssPath; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
