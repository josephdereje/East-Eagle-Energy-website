from django.shortcuts import get_object_or_404, render

from east_eagle_site.seo import SITE_URL, breadcrumb_node, build_page_schema, webpage_node

from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    featured_posts = posts.filter(is_featured=True)[:3]
    blog_url = f'{SITE_URL}/blog/'

    page_schema_json = build_page_schema(
        webpage_node(
            blog_url,
            'Blog | East Eagle Energy',
            'Solar energy tips, industry news, and product guides from East Eagle Energy.',
        ),
        {
            '@type': 'Blog',
            '@id': f'{blog_url}#blog',
            'name': 'East Eagle Energy Blog',
            'url': blog_url,
            'description': 'Solar energy tips, industry news, and product guides from East Eagle Energy.',
            'publisher': {'@id': f'{SITE_URL}/#organization'},
            'isPartOf': {'@id': f'{SITE_URL}/#website'},
        },
        breadcrumb_node([
            {'name': 'East Eagle Energy', 'url': SITE_URL + '/'},
            {'name': 'Blog', 'url': blog_url},
        ]),
    )

    return render(request, 'blog/list.html', {
        'posts': posts,
        'featured_posts': featured_posts,
        'seo_title': 'Blog | East Eagle Energy',
        'seo_description': (
            'Read the latest solar energy tips, product guides, and industry news '
            'from East Eagle Energy in Ethiopia.'
        ),
        'seo_keywords': 'solar energy blog Ethiopia, inverter tips, battery storage guide, East Eagle Energy news',
        'page_schema_json': page_schema_json,
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
    post_url = f'{SITE_URL}{post.get_absolute_url()}'

    page_schema_json = build_page_schema(
        webpage_node(post_url, f'{post.title} | East Eagle Energy', post.excerpt),
        {
            '@type': 'BlogPosting',
            'headline': post.title,
            'description': post.excerpt,
            'author': {'@type': 'Person', 'name': post.author},
            'publisher': {
                '@type': 'Organization',
                '@id': f'{SITE_URL}/#organization',
                'name': 'East Eagle Energy',
                'logo': {'@type': 'ImageObject', 'url': f'{SITE_URL}/images/logo.png'},
            },
            'datePublished': post.published_date.isoformat(),
            'dateModified': post.updated_date.isoformat(),
            'url': post_url,
            'image': og_image,
            'mainEntityOfPage': {'@id': f'{post_url}#webpage'},
            'isPartOf': {'@id': f'{SITE_URL}/#website'},
        },
        breadcrumb_node([
            {'name': 'East Eagle Energy', 'url': SITE_URL + '/'},
            {'name': 'Blog', 'url': f'{SITE_URL}/blog/'},
            {'name': post.title, 'url': post_url},
        ]),
    )

    return render(request, 'blog/detail.html', {
        'post': post,
        'related_posts': related_posts,
        'seo_title': f'{post.title} | East Eagle Energy',
        'seo_description': post.excerpt,
        'og_image': og_image,
        'og_type': 'article',
        'page_schema_json': page_schema_json,
    })
