const path = require('path');

async function getQuote(page, config, quantity, screenshotDir) {
  const result = {
    instant_quote_available: 'unclear',
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
    await page.goto('https://www.greenerprinter.com/products/custom-children%E2%80%99s-book-printing', {
      waitUntil: 'domcontentloaded',
      timeout: config.browser.timeout_ms,
    });
    await page.waitForTimeout(3000);

    // Look for quote / order link
    const links = await page.$$('a');
    let foundQuoteLink = false;
    for (const link of links) {
      const text = await link.textContent().catch(() => '');
      if (/get\s*a?\s*quote|instant\s*quote|request\s*quote|order\s*now|configure|customize/i.test(text)) {
        await link.click();
        foundQuoteLink = true;
        await page.waitForTimeout(3000);
        break;
      }
    }

    // Check body for gloss availability info
    const bodyText = await page.textContent('body').catch(() => '');

    // Check if they mention glossy interior paper
    if (/gloss\s*(?:text|interior|paper|stock)/i.test(bodyText)) {
      result.gloss_available_for_hardcover = 'yes';
      result.notes += 'Glossy interior paper mentioned on site. ';
    } else if (/recycled|uncoated|matte\s*only/i.test(bodyText)) {
      result.gloss_available_for_hardcover = 'no';
      result.notes += 'Greenerprinter focuses on eco-friendly/recycled papers — glossy interior may not be available. ';
    }

    // Try interacting with any form elements
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
        await page.waitForTimeout(1500);
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

      if (/paper|stock/i.test(label)) {
        for (const opt of options) {
          const val = await opt.textContent().catch(() => '');
          if (/gloss|coated/i.test(val)) {
            await sel.selectOption({ label: val.trim() });
            result.interior_stock_name = val.trim();
            result.interior_stock_finish = 'gloss';
            break;
          }
        }
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

    // Submit if there's a form
    const buttons = await page.$$('button, input[type="submit"]');
    for (const btn of buttons) {
      const text = await btn.textContent().catch(() => '');
      if (/calculate|get.*quote|submit|request/i.test(text)) {
        await btn.click();
        await page.waitForTimeout(5000);
        break;
      }
    }

    const ssPath = path.join(screenshotDir, `Greenerprinter_q${quantity}.png`);
    await page.screenshot({ path: ssPath, fullPage: true });
    result.screenshot_path = ssPath;

    // Try to extract pricing
    const updatedText = await page.textContent('body').catch(() => '');
    const priceMatch = updatedText.match(/(?:total|price|cost)[:\s]*\$?([\d,]+\.?\d{0,2})/i)
      || updatedText.match(/\$([\d,]+\.?\d{0,2})/);
    if (priceMatch) {
      result.print_price = '$' + priceMatch[1];
      result.status = 'partial';
    } else {
      result.status = 'manual_follow_up_needed';
      result.notes += 'Greenerprinter may require a quote request. Visit site for hardcover children\'s book, 8.5x11, 36pp, full color.';
    }

    result.quote_url = page.url();
  } catch (err) {
    result.status = 'blocked';
    result.notes = `Error: ${err.message}`;
    const ssPath = path.join(screenshotDir, `Greenerprinter_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssPath, fullPage: true }); result.screenshot_path = ssPath; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
