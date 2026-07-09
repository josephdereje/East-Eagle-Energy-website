from django.shortcuts import get_object_or_404, render

from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    featured_posts = posts.filter(is_featured=True)[:3]
    
    return render(request, 'blog/list.html', {
        'posts': posts,
        'featured_posts': featured_posts,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Get related posts (same category or recent)
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id)[:3]
    
    return render(request, 'blog/detail.html', {
        'post': post,
        'related_posts': related_posts,
    })
