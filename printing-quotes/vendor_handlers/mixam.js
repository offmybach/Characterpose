/**
 * Mixam vendor handler
 * URL: https://mixam.com/hardcoverbooks
 * Type: Instant quote calculator (JS configurator)
 *
 * Mixam has a fully interactive instant quote calculator.
 * Select product type, configure specs, and price updates live.
 */

const path = require('path');

async function getQuote(page, config, quantity, screenshotDir) {
  const specs = config.book_specs;
  const result = {
    instant_quote_available: 'yes',
    product_type_used: 'Hardcover Books',
    status: 'pending',
  };

  // Navigate to hardcover books page
  await page.goto('https://mixam.com/hardcoverbooks', {
    waitUntil: 'networkidle',
    timeout: config.browser.timeout_ms,
  });

  // Wait for the calculator to load
  await page.waitForTimeout(3000);

  // Take initial screenshot
  const ssInitial = path.join(screenshotDir, `Mixam_initial_q${quantity}.png`);
  await page.screenshot({ path: ssInitial, fullPage: false });

  // Try to find and interact with the configurator
  // Mixam uses a dynamic React/Angular configurator
  try {
    // Look for orientation selector - try landscape
    const orientationSelectors = [
      'text=Landscape',
      '[data-value="landscape"]',
      'button:has-text("Landscape")',
      'label:has-text("Landscape")',
      '.orientation-option:has-text("Landscape")',
    ];
    for (const sel of orientationSelectors) {
      try {
        const el = await page.$(sel);
        if (el) {
          await el.click();
          await page.waitForTimeout(1000);
          result.notes = (result.notes || '') + 'Selected landscape orientation. ';
          break;
        }
      } catch (_) {}
    }

    // Try to set trim size - look for size options
    // Mixam may use standard sizes. 11x8.5 landscape = 8.5x11 in landscape mode
    const sizeSelectors = [
      `text=${specs.trim_size_width}" x ${specs.trim_size_height}"`,
      `text=${specs.trim_size_height}" x ${specs.trim_size_width}"`,
      'text=8.5" x 11"',
      'text=11" x 8.5"',
      'text=Letter',
      '[data-value="8.5x11"]',
    ];
    let sizeFound = false;
    for (const sel of sizeSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(1000);
          result.trim_size_used = sel.replace('text=', '');
          sizeFound = true;
          break;
        }
      } catch (_) {}
    }

    if (!sizeFound) {
      // Try clicking on size dropdown/selector first
      const sizeDropdowns = [
        'text=Size',
        '.size-selector',
        '[data-field="size"]',
        'select[name*="size"]',
      ];
      for (const sel of sizeDropdowns) {
        try {
          const el = await page.$(sel);
          if (el && await el.isVisible()) {
            await el.click();
            await page.waitForTimeout(500);
            break;
          }
        } catch (_) {}
      }
    }

    // Try to set page count
    const pageCountSelectors = [
      'input[name*="page"]',
      'input[name*="Pages"]',
      'input[placeholder*="page"]',
      'input[type="number"]',
      '[data-field="pages"] input',
    ];
    for (const sel of pageCountSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.fill('');
          await el.fill(String(specs.page_count));
          await el.press('Tab');
          await page.waitForTimeout(1000);
          result.page_count_used = String(specs.page_count);
          break;
        }
      } catch (_) {}
    }

    // Try to set quantity
    const qtySelectors = [
      'input[name*="quantity"]',
      'input[name*="Quantity"]',
      'input[name*="qty"]',
      '#quantity',
      '[data-field="quantity"] input',
    ];
    for (const sel of qtySelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.fill('');
          await el.fill(String(quantity));
          await el.press('Tab');
          await page.waitForTimeout(1500);
          break;
        }
      } catch (_) {}
    }

    // Look for paper/stock options - specifically gloss
    const paperSelectors = [
      'text=Gloss',
      'text=gloss',
      'text=Silk',
      'text=Coated',
      '[data-value*="gloss"]',
    ];
    let glossFound = false;
    for (const sel of paperSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(1000);
          glossFound = true;
          result.interior_stock_finish = 'gloss';
          result.gloss_available_for_hardcover = 'yes';
          break;
        }
      } catch (_) {}
    }

    if (!glossFound) {
      result.gloss_available_for_hardcover = 'unclear';
      result.notes = (result.notes || '') + 'Could not confirm gloss paper selection via automation. ';
    }

    await page.waitForTimeout(2000);

    // Try to capture the price from the page
    const priceSelectors = [
      '.price',
      '.total-price',
      '.quote-price',
      '[class*="price"]',
      '[class*="Price"]',
      '[data-price]',
      '.cost',
      '.subtotal',
    ];

    let priceText = '';
    for (const sel of priceSelectors) {
      try {
        const els = await page.$$(sel);
        for (const el of els) {
          const text = await el.textContent();
          if (text && text.match(/\$[\d,.]+/)) {
            priceText = text.trim();
            break;
          }
        }
        if (priceText) break;
      } catch (_) {}
    }

    // Also try to find price by scanning visible text for dollar amounts
    if (!priceText) {
      try {
        const bodyText = await page.textContent('body');
        const priceMatch = bodyText.match(/(?:Total|Price|Cost|Quote)[:\s]*\$[\d,.]+/i);
        if (priceMatch) {
          priceText = priceMatch[0];
        }
      } catch (_) {}
    }

    if (priceText) {
      const match = priceText.match(/\$([\d,.]+)/);
      if (match) {
        result.print_price = '$' + match[1];
        result.total_price = '$' + match[1];
        result.status = 'success';
      }
    }

    // Capture page text for stock info
    try {
      const allText = await page.textContent('body');
      // Look for paper weight mentions
      const stockMatch = allText.match(/(\d+)\s*(?:lb|#|gsm)\s*(?:gloss|silk|matte|text|cover|coated)/i);
      if (stockMatch) {
        result.interior_stock_name = stockMatch[0].trim();
      }
    } catch (_) {}

    // Take final screenshot
    const ssFinal = path.join(screenshotDir, `Mixam_quote_q${quantity}.png`);
    await page.screenshot({ path: ssFinal, fullPage: false });
    result.screenshot_path = ssFinal;

    if (result.status !== 'success') {
      result.status = 'partial';
      result.notes = (result.notes || '') + 'Calculator loaded but could not fully extract price. May need manual interaction with the JS configurator. ';
      result.quote_url = 'https://mixam.com/hardcoverbooks';
    }

    result.binding_used = 'hardcover';
    result.interior_color = 'full color';

  } catch (err) {
    result.status = 'blocked';
    result.notes = `Automation error: ${err.message}`;
    const ssErr = path.join(screenshotDir, `Mixam_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssErr, fullPage: true }); result.screenshot_path = ssErr; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
