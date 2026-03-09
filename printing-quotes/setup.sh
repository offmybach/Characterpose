#!/usr/bin/env bash
# Setup script for the printing quote collector
# Run this once on a new machine to install dependencies

set -e

echo "=== Printing Quote Collector Setup ==="
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is required. Install from https://nodejs.org/"
    exit 1
fi

echo "Node.js: $(node --version)"

# Install npm dependencies
echo ""
echo "Installing npm dependencies..."
npm install

# Install Playwright browser
echo ""
echo "Installing Chromium for Playwright..."
npx playwright install chromium

echo ""
echo "=== Setup complete! ==="
echo ""
echo "To run the quote collector:"
echo "  node main.js"
echo ""
echo "To run with visible browser (non-headless):"
echo "  Edit config.json and set browser.headless to false"
echo "  node main.js"
