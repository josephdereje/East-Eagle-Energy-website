from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from pathlib import Path
import re

from django.conf import settings


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


class HeroSlide(models.Model):
    """Homepage hero carousel slides — managed via admin."""
    eyebrow = models.CharField(max_length=100, blank=True, help_text='Small label above title')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=350, blank=True)
    image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True,
        help_text='Background image (recommended 1920×800px)',
    )
    gradient = models.CharField(
        max_length=300,
        default='linear-gradient(135deg, #1B365D 0%, #2E6EB3 50%, #F39200 100%)',
        help_text='CSS gradient overlay when no image, or over image',
    )
    primary_btn_text = models.CharField(max_length=50, default='View Products')
    primary_btn_url = models.CharField(max_length=200, default='/products/')
    secondary_btn_text = models.CharField(max_length=50, blank=True)
    secondary_btn_url = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        """Use /images/hero/ static files when available (works in dev + production)."""
        if not self.image:
            return ''

        hero_dir = Path(settings.BASE_DIR) / 'images' / 'hero'
        media_name = Path(self.image.name).name
        candidates = [media_name]

        match = re.match(r'^(slide-[^_]+)(?:_[A-Za-z0-9]+)?(\.[^.]+)$', media_name)
        if match:
            candidates.append(f'{match.group(1)}{match.group(2)}')

        for name in dict.fromkeys(candidates):
            if (hero_dir / name).exists():
                return f'/images/hero/{name}'

        return self.image.url


class AboutPage(models.Model):
    """Singleton — edit About page hero & mission in admin."""
    hero_eyebrow = models.CharField(max_length=100, default='About East Eagle Energy')
    hero_title = models.CharField(max_length=200, default='Energy That Never Grows Weary')
    hero_subtitle = models.CharField(
        max_length=350,
        default='Global solar, storage, and power solutions — built for reliability since 2022.',
    )
    aims_intro = models.TextField(
        default='East Eagle Energy was founded with a clear purpose: to make dependable, clean energy accessible to homes, businesses, and industries worldwide.',
    )
    mission_eyebrow = models.CharField(max_length=100, default='Our Mission')
    mission_title = models.CharField(max_length=200, default='Resilient Energy for Every Project')
    mission_text = models.TextField(
        default=(
            'To supply energy solutions — inverters, battery storage, solar panels, and EV charging systems — '
            'that remain resilient and dependable over time. We believe power should never grow weary, '
            'whether for a family home, a commercial building, or an industrial facility.'
        ),
    )
    mission_quote = models.CharField(max_length=200, default='Energy That Never Grows Weary.')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Page'

    def __str__(self):
        return 'About Page Content'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutValue(models.Model):
    """Core values / aims shown on About page."""
    icon = models.CharField(max_length=60, default='fa-globe', help_text='Font Awesome class, e.g. fa-globe')
    title = models.CharField(max_length=120)
    description = models.TextField()
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'About Value'
        verbose_name_plural = 'About Values'

    def __str__(self):
        return self.title


class AboutMilestone(models.Model):
    """Timeline milestones on About page."""
    year = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    description = models.TextField()
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'About Milestone'
        verbose_name_plural = 'About Milestones'

    def __str__(self):
        return f'{self.year} — {self.title}'


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
