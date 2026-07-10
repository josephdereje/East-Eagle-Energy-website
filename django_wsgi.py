import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'east_eagle_site.settings')

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_DIR, '.env'))
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
