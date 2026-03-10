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
    await page.goto('https://theworldpublishingcompany.com/children-book-printing', {
      waitUntil: 'domcontentloaded',
      timeout: config.browser.timeout_ms,
    });
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent('body').catch(() => '');

    // Check for gloss/hardcover mentions
    if (/gloss|coated/i.test(bodyText)) {
      result.gloss_available_for_hardcover = 'yes';
      result.notes += 'Glossy/coated paper mentioned. ';
    }

    // Look for quote/pricing link
    const links = await page.$$('a');
    for (const link of links) {
      const text = await link.textContent().catch(() => '');
      if (/get\s*a?\s*quote|request\s*quote|pricing|calculator|free\s*quote/i.test(text)) {
        const href = await link.getAttribute('href').catch(() => '');
        if (href && !href.includes('mailto')) {
          result.quote_url = href.startsWith('http') ? href : `https://theworldpublishingcompany.com${href}`;
          await link.click();
          await page.waitForTimeout(3000);
          break;
        }
      }
    }

    // Try form interaction
    const allSelects = await page.$$('select');
    for (const sel of allSelects) {
      const name = await sel.getAttribute('name').catch(() => '') || '';
      const id = await sel.getAttribute('id').catch(() => '') || '';
      const label = (name + ' ' + id).toLowerCase();
      const options = await sel.$$('option');

      if (/bind|cover|type|product/i.test(label)) {
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

    // Try submit
    const buttons = await page.$$('button, input[type="submit"]');
    for (const btn of buttons) {
      const text = await btn.textContent().catch(() => '');
      if (/calculate|get.*quote|submit|request/i.test(text)) {
        await btn.click();
        await page.waitForTimeout(5000);
        break;
      }
    }

    const ssPath = path.join(screenshotDir, `WorldPublishing_q${quantity}.png`);
    await page.screenshot({ path: ssPath, fullPage: true });
    result.screenshot_path = ssPath;

    // Try to extract pricing
    const updatedText = await page.textContent('body').catch(() => '');
    const priceMatch = updatedText.match(/(?:total|price|cost)[:\s]*\$?([\d,]+\.?\d{0,2})/i);
    if (priceMatch) {
      result.print_price = '$' + priceMatch[1];
      result.status = 'partial';
    } else {
      result.status = 'manual_follow_up_needed';
      result.notes += 'The World Publishing Company — contact for custom quote: hardcover children\'s book, 11x8.5, 36pp, full color, 100# gloss text.';
    }

    result.quote_url = result.quote_url || page.url();
  } catch (err) {
    result.status = 'blocked';
    result.notes = `Error: ${err.message}`;
    const ssPath = path.join(screenshotDir, `WorldPublishing_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssPath, fullPage: true }); result.screenshot_path = ssPath; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
