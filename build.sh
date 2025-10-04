#!/usr/bin/env bash
# Build script for Render.com deployment

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
# Install chromium without --with-deps (Render free tier has no root access)
playwright install chromium

echo "Verifying Chromium installation..."
python3 -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); print(f'Chromium path: {p.chromium.executable_path}'); p.stop()" || echo "Warning: Could not verify Chromium"

echo "Build completed successfully!"
