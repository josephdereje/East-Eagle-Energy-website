import json

from django.shortcuts import get_object_or_404, render

from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    featured_posts = posts.filter(is_featured=True)[:3]

    schema = {
        '@context': 'https://schema.org',
        '@type': 'Blog',
        'name': 'East Eagle Energy Blog',
        'url': 'https://www.easteagleenergy.com/blog/',
        'description': 'Solar energy tips, industry news, and product guides from East Eagle Energy Ethiopia.',
        'publisher': {'@type': 'Organization', 'name': 'East Eagle Energy'},
    }

    return render(request, 'blog/list.html', {
        'posts': posts,
        'featured_posts': featured_posts,
        'seo_title': 'Blog | East Eagle Energy',
        'seo_description': (
            'Read the latest solar energy tips, product guides, and industry news '
            'from East Eagle Energy in Ethiopia.'
        ),
        'seo_keywords': 'solar energy blog Ethiopia, inverter tips, battery storage guide, East Eagle Energy news',
        'schema_json': json.dumps(schema),
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    post.views_count += 1
    post.save(update_fields=['views_count'])

    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id)[:3]

    og_image = (
        f'https://www.easteagleenergy.com{post.featured_image.url}'
        if post.featured_image else 'https://www.easteagleenergy.com/images/logo.png'
    )
    schema = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': post.title,
        'description': post.excerpt,
        'author': {'@type': 'Person', 'name': post.author},
        'publisher': {
            '@type': 'Organization',
            'name': 'East Eagle Energy',
            'logo': {'@type': 'ImageObject', 'url': 'https://www.easteagleenergy.com/images/logo.png'},
        },
        'datePublished': post.published_date.isoformat(),
        'dateModified': post.updated_date.isoformat(),
        'url': f'https://www.easteagleenergy.com{post.get_absolute_url()}',
        'image': og_image,
        'mainEntityOfPage': {
            '@type': 'WebPage',
            '@id': f'https://www.easteagleenergy.com{post.get_absolute_url()}',
        },
    }

    return render(request, 'blog/detail.html', {
        'post': post,
        'related_posts': related_posts,
        'seo_title': f'{post.title} | East Eagle Energy',
        'seo_description': post.excerpt,
        'og_image': og_image,
        'og_type': 'article',
        'schema_json': json.dumps(schema),
    })
