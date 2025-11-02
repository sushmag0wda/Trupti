#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py create_superuser

# Collect static files
python manage.py collectstatic --no-input
