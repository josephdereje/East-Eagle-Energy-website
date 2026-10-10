import os

from .seo import site_schema_json


def seo_branding(request):
    return {
        'site_schema_json': site_schema_json(),
        'site_brand_name': 'East Eagle Energy',
        'app_store_url': os.getenv('APP_STORE_URL', 'https://apps.apple.com/'),
        'play_store_url': os.getenv('PLAY_STORE_URL', 'https://play.google.com/store'),
    }
