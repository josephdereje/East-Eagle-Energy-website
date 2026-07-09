from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path, re_path
from django.views.static import serve

from contact.forms import ContactInquiryForm
from east_eagle_site import settings
from products.models import Product
from blog.models import HomepageAd, BlogPost

admin.site.site_header = 'East Eagle Energy Admin'
admin.site.site_title = 'East Eagle Energy'
admin.site.index_title = 'Site Management'


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    homepage_ads = HomepageAd.objects.filter(is_active=True)[:3]
    latest_blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    return render(
        request,
        'home.html',
        {
            'featured_products': featured_products,
            'homepage_ads': homepage_ads,
            'latest_blog_posts': latest_blog_posts,
            'contact_form': ContactInquiryForm(),
        },
    )


urlpatterns = [
    path('admin/', admin.site.urls),
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
