#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories with proper permissions
mkdir -p static
mkdir -p staticfiles
mkdir -p media

# Set proper permissions
chmod -R 755 static
chmod -R 755 staticfiles
chmod -R 755 media

# Make and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
export DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
export DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
export DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin123}

python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 2>/dev/null || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "Static files collected successfully"
