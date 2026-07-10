import json

from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import include, path, re_path
from django.views.static import serve

from contact.forms import ContactInquiryForm
from products.models import Product
from blog.models import HomepageAd, BlogPost
from east_eagle_site.sitemaps import sitemaps

admin.site.site_header = 'East Eagle Energy Admin'
admin.site.site_title = 'East Eagle Energy'
admin.site.index_title = 'Site Management'


def health_check(request):
    return render(request, 'health.html', {}, content_type='text/html')


def robots_txt(request):
    content = render_to_string('robots.txt')
    return HttpResponse(content, content_type='text/plain')


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    homepage_ads = HomepageAd.objects.filter(is_active=True)[:3]
    latest_blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': 'East Eagle Energy',
        'url': 'https://www.easteagleenergy.com',
        'logo': 'https://www.easteagleenergy.com/images/logo.png',
        'description': (
            'East Eagle Energy specializes in solar inverters, LiFePO4 batteries, '
            'and energy storage systems for homes and businesses across Ethiopia.'
        ),
        'foundingDate': '2022',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': 'Century Executive Tower, 12-Room Number F12/06',
            'addressLocality': 'Addis Ababa',
            'addressCountry': 'ET',
        },
        'telephone': '+251933219802',
    }

    return render(
        request,
        'home.html',
        {
            'featured_products': featured_products,
            'homepage_ads': homepage_ads,
            'latest_blog_posts': latest_blog_posts,
            'contact_form': ContactInquiryForm(),
            'seo_title': 'East Eagle Energy — Energy That Never Grows Weary',
            'seo_description': (
                'East Eagle Energy supplies solar inverters, LiFePO4 batteries, and '
                'energy storage systems for homes and businesses across Ethiopia. '
                'Based in Addis Ababa since 2022.'
            ),
            'seo_keywords': (
                'solar energy Ethiopia, inverter Ethiopia, battery storage Addis Ababa, '
                'East Eagle Energy, LiFePO4 battery, Deye inverter, Growatt Ethiopia, '
                'BESS Ethiopia, solar panels Ethiopia'
            ),
            'schema_json': json.dumps(schema),
        },
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', home, name='home'),
    path('products/', include('products.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^css/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'css'}),
        re_path(r'^js/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'js'}),
        re_path(r'^images/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'images'}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
