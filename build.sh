#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories with proper permissions
echo "Creating directories..."
mkdir -p static staticfiles media
chmod -R 755 static staticfiles media

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Setting up superuser..."
export DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
export DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
export DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin123}

# Try to create superuser, ignore if it already exists
python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" 2>/dev/null || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Set proper permissions for static files
chmod -R 755 staticfiles/

echo "Build completed successfully!"
