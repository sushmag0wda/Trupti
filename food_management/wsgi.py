"""
WSGI config for food_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_management.settings')

# This application object is used by any WSGI server configured to use this file.
application = get_wsgi_application()

# Add WhiteNoise for serving static files in production
application = WhiteNoise(
    application,
    root=os.path.join(Path(__file__).resolve().parent.parent, 'staticfiles'),
    prefix='/static/'
)
application.add_files(os.path.join(Path(__file__).resolve().parent.parent, 'static'), prefix='/static/')
application.add_files(os.path.join(Path(__file__).resolve().parent.parent, 'media'), prefix='/media/')
