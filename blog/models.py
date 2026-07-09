from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt = models.CharField(max_length=300, help_text='Short summary for blog list page')
    content = models.TextField()
    author = models.CharField(max_length=100, default='East Eagle Energy')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Featured posts show on homepage')
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class HomepageAd(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='ads/')
    link_url = models.URLField(blank=True, help_text='Link to product page or external URL')
    button_text = models.CharField(max_length=50, default='Learn More')
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text='Lower numbers appear first')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Homepage Ad/Banner'
        verbose_name_plural = 'Homepage Ads/Banners'
    
    def __str__(self):
        return self.title
