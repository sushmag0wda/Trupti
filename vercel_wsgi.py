import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_management.settings')

# Import and configure the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
