#!/usr/bin/env bash
# Build script for Render.com deployment

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install chromium

echo "Installing system dependencies for Playwright..."
playwright install-deps chromium

echo "Build completed successfully!"
