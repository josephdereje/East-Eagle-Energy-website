import os
import sys

# Add the project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'east_eagle_site.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
