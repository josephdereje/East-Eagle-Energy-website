from django.contrib import admin

from .models import Product, ProductSidebarSection, ProductSidebarImage, ProductType, EssSubType


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
