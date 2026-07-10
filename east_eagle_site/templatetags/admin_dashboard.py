from django import template

register = template.Library()


@register.simple_tag
def admin_dashboard_stats():
    from blog.models import BlogPost, HomepageAd
    from contact.models import ContactInquiry
    from products.models import Product

    return {
        'products': Product.objects.filter(is_active=True).count(),
        'products_total': Product.objects.count(),
        'blog_posts': BlogPost.objects.filter(is_published=True).count(),
        'blog_drafts': BlogPost.objects.filter(is_published=False).count(),
        'inquiries': ContactInquiry.objects.count(),
        'homepage_ads': HomepageAd.objects.filter(is_active=True).count(),
    }
