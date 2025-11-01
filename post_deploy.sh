#!/bin/bash
# This script runs after deployment
python manage.py collectstatic --noinput
python manage.py migrate
