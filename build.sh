#!/usr/bin/env bash
# Build script for Render.com deployment

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright Chromium browser..."
playwright install --with-deps chromium 2>/dev/null || playwright install chromium

# Note: Trying --with-deps first, but falling back to basic install if it fails
# Render.com has most system dependencies pre-installed

echo "Build completed successfully!"
