/**
 * Books.by vendor handler
 * URL: https://books.by / https://try.books.by
 * Type: Print-on-demand platform (NOT a traditional bulk printer)
 *
 * Books.by is a POD storefront platform for authors, not a traditional
 * book printer that offers bulk quotes. They do not appear to have a
 * hardcover option or a bulk quantity calculator.
 *
 * This handler inspects the site and flags limitations.
 */

const path = require('path');

async function getQuote(page, config, quantity, screenshotDir) {
  const result = {
    instant_quote_available: 'no',
    product_type_used: 'Print-on-Demand Storefront',
    status: 'pending',
  };

  try {
    // Check their printing/formats page first
    await page.goto('https://try.books.by/printing-book-sizes-formats', {
      waitUntil: 'networkidle',
      timeout: config.browser.timeout_ms,
    });

    await page.waitForTimeout(3000);

    const ssFormats = path.join(screenshotDir, `BooksBY_formats_q${quantity}.png`);
    await page.screenshot({ path: ssFormats, fullPage: false });

    const bodyText = await page.textContent('body');

    // Check for hardcover mention
    const hasHardcover = /hardcover|hard\s*cover|case\s*bound|casebound/i.test(bodyText);
    // Check for gloss mention
    const hasGloss = /gloss/i.test(bodyText);
    // Check for bulk/quantity pricing
    const hasBulk = /bulk|quantity|wholesale|500|250/i.test(bodyText);

    if (!hasHardcover) {
      result.status = 'rejected_non_gloss';
      result.gloss_available_for_hardcover = 'no';
      result.notes = 'Books.by is a print-on-demand storefront platform. No hardcover option found. No bulk quantity pricing available. This is not a traditional book printer — it is an author storefront/POD service similar to Lulu or Amazon KDP. Not suitable for bulk hardcover children\'s book printing.';
      result.screenshot_path = ssFormats;
      result.quote_url = 'https://try.books.by/printing-book-sizes-formats';
      return result;
    }

    // Check pricing page
    await page.goto('https://try.books.by/pricing', {
      waitUntil: 'networkidle',
      timeout: config.browser.timeout_ms,
    });

    await page.waitForTimeout(2000);

    const ssPricing = path.join(screenshotDir, `BooksBY_pricing_q${quantity}.png`);
    await page.screenshot({ path: ssPricing, fullPage: false });

    const pricingText = await page.textContent('body');

    // Check for per-unit pricing info
    const priceMatch = pricingText.match(/\$([\d.]+)\s*(?:per|\/)\s*(?:book|copy)/i);

    result.binding_used = hasHardcover ? 'hardcover (if available)' : 'paperback only';
    result.gloss_available_for_hardcover = hasGloss ? 'unclear' : 'no';
    result.interior_stock_finish = hasGloss ? 'unclear' : 'unknown';
    result.screenshot_path = ssPricing;
    result.quote_url = 'https://try.books.by/pricing';

    if (!hasBulk) {
      result.status = 'manual_follow_up_needed';
      result.notes = 'Books.by is a POD platform with subscription pricing, not a bulk printer. No bulk quantity calculator found. ';
      if (!hasHardcover) {
        result.notes += 'No hardcover option detected. ';
      }
      if (!hasGloss) {
        result.notes += 'No gloss paper option detected. ';
        result.status = 'rejected_non_gloss';
      }
      result.notes += `MANUAL FOLLOW-UP: Contact Books.by support to ask about bulk hardcover printing with glossy interior. Visit https://try.books.by/pricing for current plans. `;
    }

  } catch (err) {
    result.status = 'blocked';
    result.notes = `Could not access Books.by: ${err.message}`;
    const ssErr = path.join(screenshotDir, `BooksBY_error_q${quantity}.png`);
    try { await page.screenshot({ path: ssErr, fullPage: true }); result.screenshot_path = ssErr; } catch (_) {}
  }

  return result;
}

module.exports = { getQuote };
