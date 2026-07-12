from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogPost
from products.models import Product, ProductCategory


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['home', 'about', 'products:list', 'blog:list', 'contact:page']

    def location(self, item):
        return reverse(item)


class ProductCategorySitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [c.value for c in ProductCategory]

    def location(self, item):
        return reverse('products:category', kwargs={'category': item})


class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    'static': StaticViewSitemap,
    'product_categories': ProductCategorySitemap,
    'products': ProductSitemap,
    'blog': BlogSitemap,
}
