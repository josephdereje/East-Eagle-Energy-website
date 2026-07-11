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
from blog.models import HomepageAd, BlogPost, HeroSlide
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
    hero_slides = HeroSlide.objects.filter(is_active=True)
    
    # Schema.org structured data with both Organization and WebSite
    schema = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Organization',
                '@id': 'https://www.easteagleenergy.com/#organization',
                'name': 'East Eagle Energy',
                'url': 'https://www.easteagleenergy.com',
                'logo': {
                    '@type': 'ImageObject',
                    'url': 'https://www.easteagleenergy.com/images/logo.png',
                    'width': 250,
                    'height': 160,
                },
                'description': (
                    'East Eagle Energy specializes in solar inverters, LiFePO4 batteries, '
                    'and energy storage systems for homes and businesses worldwide. '
                    'Energy That Never Grows Weary.'
                ),
                'foundingDate': '2022',
                'address': {
                    '@type': 'PostalAddress',
                    'streetAddress': 'Century Executive Tower, 12-Room Number F12/06',
                    'addressLocality': 'Addis Ababa',
                    'addressCountry': 'ET',
                },
                'telephone': '+251933219802',
                'sameAs': [
                    'https://www.facebook.com/easteagleenergy',
                    'https://www.linkedin.com/company/easteagleenergy',
                ],
            },
            {
                '@type': 'WebSite',
                '@id': 'https://www.easteagleenergy.com/#website',
                'url': 'https://www.easteagleenergy.com',
                'name': 'East Eagle Energy',
                'description': 'Global provider of solar energy solutions',
                'publisher': {
                    '@id': 'https://www.easteagleenergy.com/#organization'
                },
                'potentialAction': {
                    '@type': 'SearchAction',
                    'target': 'https://www.easteagleenergy.com/products/search/?q={search_term_string}',
                    'query-input': 'required name=search_term_string',
                },
            },
        ],
    }

    return render(
        request,
        'home.html',
        {
            'featured_products': featured_products,
            'homepage_ads': homepage_ads,
            'latest_blog_posts': latest_blog_posts,
            'hero_slides': hero_slides,
            'contact_form': ContactInquiryForm(),
            'seo_title': 'East Eagle Energy | Energy Solutions',
            'seo_description': (
                'East Eagle Energy - Global provider of solar inverters, LiFePO4 batteries, and '
                'energy storage systems. Reliable solar power solutions for homes and businesses '
                'worldwide. Energy That Never Grows Weary.'
            ),
            'seo_keywords': (
                'East Eagle Energy, solar energy, solar inverter, battery storage, '
                'energy solutions, LiFePO4 battery, Deye inverter, Growatt, '
                'BESS, renewable energy, global solar solutions'
            ),
            'schema_json': json.dumps(schema),
        },
    )


def about(request):
    schema = {
        '@context': 'https://schema.org',
        '@type': 'AboutPage',
        'name': 'About East Eagle Energy',
        'description': (
            'East Eagle Energy — global provider of solar inverters, LiFePO4 batteries, '
            'and energy storage systems. Energy That Never Grows Weary.'
        ),
        'url': 'https://www.easteagleenergy.com/about/',
    }
    return render(
        request,
        'about.html',
        {
            'seo_title': 'About Us | East Eagle Energy',
            'seo_description': (
                'Learn about East Eagle Energy — our mission, core aims, and growth '
                'as a global energy storage and solar solutions provider since 2022.'
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
    path('about/', about, name='about'),
    path('products/', include('products.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
]

# Templates load /css/, /js/, /images/ (not /static/). Serve these in
# production too so updates from git pull apply without relying only on
# a separate public_html copy. Media stays DEBUG-only when DEBUG is True.
urlpatterns += [
    re_path(r'^css/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'css'}),
    re_path(r'^js/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'js'}),
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'images'}),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
