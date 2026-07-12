from .seo import site_schema_json


def seo_branding(request):
    return {
        'site_schema_json': site_schema_json(),
        'site_brand_name': 'East Eagle Energy',
    }
