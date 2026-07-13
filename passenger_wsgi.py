import os
import sys
import traceback

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)

LOG_FILE = os.path.join(PROJECT_DIR, 'ERROR_LOG.txt')

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_production')

    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(PROJECT_DIR, '.env'))
    except ImportError:
        pass

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

except Exception:
    error_text = traceback.format_exc()
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(error_text)

    def application(environ, start_response):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(error_text)
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [error_text.encode('utf-8')]
