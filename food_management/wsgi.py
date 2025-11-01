"""WSGI config for food_management project."""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_management.settings")

application = get_wsgi_application()

# Serve static files using WhiteNoise
application = WhiteNoise(
    application,
    root=os.path.join(Path(__file__).parent.parent, 'staticfiles'),
    prefix='/static/'
)
application.add_files(os.path.join(Path(__file__).parent.parent, 'static'), prefix='/static/')
application.add_files(os.path.join(Path(__file__).parent.parent, 'media'), prefix='/media/')
