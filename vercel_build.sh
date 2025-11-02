#!/bin/bash

# Exit on error
set -e

echo "===== Starting Build Process ====="

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "===== Build Process Complete ====="

# Collect static files
echo "Collecting static files..."
mkdir -p staticfiles
python manage.py collectstatic --noinput

echo "Build completed successfully!"
