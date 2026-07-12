from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    ProductSidebarSection,
    ProductSidebarImage,
    RecommendedProduct,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'label', 'display_order', 'is_active')


class ProductSidebarImageInline(admin.TabularInline):
    model = ProductSidebarImage
    extra = 1
    fields = ('image', 'title', 'caption', 'link_url', 'display_order', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'category', 'voltage_type', 'ess_sub_type', 'price', 'is_featured', 'is_active')
    list_filter = ('product_type', 'category', 'voltage_type', 'ess_sub_type', 'is_featured', 'is_active')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'product_type', 'category', 'voltage_type', 'ess_sub_type')
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'image', 'price')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )


@admin.register(ProductSidebarSection)
class ProductSidebarSectionAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'is_active', 'display_order')
    list_filter = ('category', 'is_active')
    list_editable = ('is_active', 'display_order')
    inlines = [ProductSidebarImageInline]
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'description', 'display_order', 'is_active')
        }),
    )


@admin.register(RecommendedProduct)
class RecommendedProductAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'badge', 'product', 'is_active', 'display_order', 'created_at')
    list_filter = ('badge', 'is_active')
    list_editable = ('is_active', 'display_order')
    search_fields = ('title', 'subtitle', 'product__name')
    autocomplete_fields = ('product',)
    fieldsets = (
        ('Link to catalog (optional)', {
            'fields': ('product',),
            'description': 'Pick a product to auto-fill title/image/link, or leave blank for a custom promo.',
        }),
        ('Promo content', {
            'fields': ('title', 'subtitle', 'badge', 'image', 'link_url', 'button_text'),
        }),
        ('Display', {
            'fields': ('display_order', 'is_active'),
        }),
    )
