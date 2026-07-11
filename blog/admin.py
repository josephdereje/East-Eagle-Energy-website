from django.contrib import admin

from .models import BlogPost, HeroSlide, HomepageAd


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published', 'is_featured', 'views_count')
    list_filter = ('is_published', 'is_featured', 'published_date')
    search_fields = ('title', 'excerpt', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('views_count', 'published_date', 'updated_date')

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'excerpt', 'content', 'featured_image')
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('views_count', 'published_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'eyebrow', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'display_order')
    search_fields = ('title', 'subtitle', 'eyebrow')
    fieldsets = (
        ('Slide Content', {
            'fields': ('eyebrow', 'title', 'subtitle', 'image', 'gradient')
        }),
        ('Buttons', {
            'fields': (
                'primary_btn_text', 'primary_btn_url',
                'secondary_btn_text', 'secondary_btn_url',
            )
        }),
        ('Display', {
            'fields': ('display_order', 'is_active')
        }),
    )


@admin.register(HomepageAd)
class HomepageAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active', 'display_order')
    search_fields = ('title', 'subtitle')
