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
    // Lightning Press has an instant price calculator
    await page.goto('https://lightning-press.com/book-printing/price-and-cost-example/', {
      waitUntil: 'domcontentloaded',
      timeout: config.browser.timeout_ms,
    });
    await page.waitForTimeout(3000);

    // Look for a calculator link/button
    const calcLinks = await page.$$('a');
    for (const link of calcLinks) {
      const text = await link.textContent().catch(() => '');
      if (/calculator|instant\s*price|get\s*price|quote/i.test(text)) {
        const href = await link.getAttribute('href').catch(() => '');
        if (href) {
          await page.goto(href.startsWith('http') ? href : `https://lightning-press.com${href}`, {
            waitUntil: 'domcontentloaded',
            timeout: config.browser.timeout_ms,
          });
          break;
        }
      }
    }
    await page.waitForTimeout(3000);

    // Interact with calculator form
    const allSelects = await page.$$('select');
    for (const sel of allSelects) {
      const name = await sel.getAttribute('name').catch(() => '') || '';
      const id = await sel.getAttribute('id').catch(() => '') || '';
      const label = (name + ' ' + id).toLowerCase();
      const options = await sel.$$('option');

      if (/bind|cover|type/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/hard\s*cover|case\s*bound/i.test(val)) {
            await sel.selectOption({ label: val.trim() });
            break;
          }
        }
        await page.waitForTimeout(2000);
      }

      if (/size|trim/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/11\s*[x×]\s*8\.?5|8\.?5\s*[x×]\s*11/i.test(val)) {
            await sel.selectOption({ label: val.trim() });
            break;
          }
        }
        await page.waitForTimeout(1500);
      }

      if (/color|ink|interior/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/full\s*color|4.*4|color/i.test(val)) {
            await sel.selectOption({ label: val.trim() });
            break;
          }
        }
        await page.waitForTimeout(1500);
      }

      if (/paper|stock/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/gloss|100\s*#|100\s*lb|coated/i.test(val)) {
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

    // Fill page count and quantity
    const allInputs = await page.$$('input[type="text"], input[type="number"], input:not([type])');
    for (const inp of allInputs) {
      const name = await inp.getAttribute('name').catch(() => '') || '';
      const id = await inp.getAttribute('id').catch(() => '') || '';
      const placeholder = await inp.getAttribute('placeholder').catch(() => '') || '';
      const combined = (name + ' ' + id + ' ' + placeholder).toLowerCase();

      if (/page|pg/i.test(combined) && !/email|name|phone/i.test(combined)) {
        await inp.fill(String(config.book_specs.page_count));
        await page.waitForTimeout(500);
      }
      if (/qty|quantity|copies/i.test(combined) && !/page|pg/i.test(combined)) {
        await inp.fill(String(quantity));
        await page.waitForTimeout(500);
      }
    }

    // Submit
    const buttons = await page.$$('button, input[type="submit"], a.btn');
    for (const btn of buttons) {
      const text = await btn.textContent().catch(() => '');
      if (/calculate|get.*price|submit|quote/i.test(text)) {
        await btn.click();
        break;
      }
    }
    await page.waitForTimeout(5000);

    const ssPath = path.join(screenshotDir, `LightningPress_q${quantity}.png`);
    await page.screenshot({ path: ssPath, fullPage: true });
    result.screenshot_path = ssPath;

    const bodyText = await page.textContent('body').catch(() => '');

    // Extract pricing
    const priceMatch = bodyText.match(/(?:total|price|cost)[:\s]*\$?([\d,]+\.?\d{0,2})/i)
      || bodyText.match(/\$([\d,]+\.?\d{0,2})/);
    if (priceMatch) {
      result.print_price = '$' + priceMatch[1];
    }

    const perUnitMatch = bodyText.match(/(?:per\s*(?:book|copy|unit))[:\s]*\$?([\d.]+)/i);
    if (perUnitMatch) {
      result.notes += `Per unit: $${perUnitMatch[1]}. `;
    }

    const shipMatch = bodyText.match(/shipping[:\s]*\$?([\d,]+\.?\d{0,2})/i);
    if (shipMatch) {
      result.shipping_price = '$' + shipMatch[1];
    }

    const turnMatch = bodyText.match(/(\d+[-–]\d+\s*(?:business\s*)?days?)/i);
    if (turnMatch) {
      result.turnaround_time = turnMatch[1];
    }

    if (result.print_price) {
      result.status = result.shipping_price ? 'success' : 'partial';
    } else {
      result.status = 'manual_follow_up_needed';
      result.notes = 'Could not extract price. Lightning Press has an online calculator — visit site for 11x8.5 landscape hardcover, 36pp, full color, gloss interior.';
    }

    result.quote_url = page.url();
  } catch (err) {
    result.status = 'blocked';
    result.notes = `Error: ${err.message}`;
    const ssPath = path.join(screenshotDir, `LightningPress_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssPath, fullPage: true }); result.screenshot_path = ssPath; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
