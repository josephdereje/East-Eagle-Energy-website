import json

from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Product, ProductCategory, VoltageType, ProductSidebarSection


def product_list(request, category=None, voltage_type=None):
    products = Product.objects.filter(is_active=True)
    active_category = category or 'all'
    active_voltage = voltage_type or 'all'
    sidebar_section = None

    # Filter by category
    if category and category != 'all':
        if category not in ProductCategory.values:
            category = 'all'
        else:
            products = products.filter(category=category)
            active_category = category
            # Get sidebar content for this category
            try:
                sidebar_section = ProductSidebarSection.objects.get(
                    category=category, 
                    is_active=True
                )
            except ProductSidebarSection.DoesNotExist:
                pass
    
    # Filter by voltage type (for residential products)
    if voltage_type and voltage_type != 'all' and category == 'residential':
        if voltage_type in VoltageType.values:
            products = products.filter(voltage_type=voltage_type)
            active_voltage = voltage_type

    # Build categories list
    categories = [
        {'slug': 'all', 'label': 'All Products'},
        *[
            {'slug': value, 'label': label}
            for value, label in ProductCategory.choices
        ],
    ]
    
    # Build voltage types (for residential sidebar)
    voltage_types = []
    if category == 'residential':
        voltage_types = [
            {'slug': 'all', 'label': 'All Types'},
            {'slug': VoltageType.LOW_VOLTAGE, 'label': 'Low Voltage'},
            {'slug': VoltageType.HIGH_VOLTAGE, 'label': 'High Voltage'},
        ]

    # SEO
    if category and category != 'all':
        cat_label = next((c['label'] for c in categories if c['slug'] == category), 'Products')
        seo_title = f'{cat_label} | East Eagle Energy'
        seo_description = (
            f'Browse East Eagle Energy {cat_label} — solar inverters, batteries, '
            f'and energy storage systems for Ethiopia.'
        )
    else:
        seo_title = 'Products | East Eagle Energy'
        seo_description = (
            'Explore all East Eagle Energy products: residential solar inverters, '
            'C&I BESS, and ESS solutions for Ethiopia.'
        )

    schema = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': seo_title,
        'url': 'https://www.easteagleenergy.com/products/',
        'numberOfItems': products.count(),
    }

    return render(
        request,
        'products/list.html',
        {
            'products': products,
            'categories': categories,
            'voltage_types': voltage_types,
            'active_category': active_category,
            'active_voltage': active_voltage,
            'sidebar_section': sidebar_section,
            'seo_title': seo_title,
            'seo_description': seo_description,
            'seo_keywords': 'solar inverter Ethiopia, battery storage Ethiopia, BESS Ethiopia, East Eagle Energy products',
            'schema_json': json.dumps(schema),
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get sidebar for this product's category
    sidebar_section = None
    try:
        sidebar_section = ProductSidebarSection.objects.get(
            category=product.category,
            is_active=True
        )
    except ProductSidebarSection.DoesNotExist:
        pass
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    og_image = (
        f'https://www.easteagleenergy.com{product.image.url}'
        if product.image else 'https://www.easteagleenergy.com/images/logo.png'
    )
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': product.name,
        'description': product.short_description or product.description[:160],
        'brand': {'@type': 'Brand', 'name': 'East Eagle Energy'},
        'url': f'https://www.easteagleenergy.com{product.get_absolute_url()}',
        'image': og_image,
        'offers': {
            '@type': 'Offer',
            'availability': 'https://schema.org/InStock',
            'priceCurrency': 'ETB',
            'seller': {'@type': 'Organization', 'name': 'East Eagle Energy'},
        },
    }
    if product.price:
        schema['offers']['price'] = str(product.price)

    return render(
        request,
        'products/detail.html',
        {
            'product': product,
            'related_products': related_products,
            'sidebar_section': sidebar_section,
            'seo_title': f'{product.name} | East Eagle Energy',
            'seo_description': product.short_description or product.description[:160],
            'og_image': og_image,
            'og_type': 'product',
            'schema_json': json.dumps(schema),
        }
    )


def product_search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)
    
    if query:
        # Search in name, short_description, description, and category
        products = products.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    
    # Count results
    result_count = products.count()
    
    # Build categories for filter
    categories = [
        {'slug': 'all', 'label': 'All Products'},
        *[
            {'slug': value, 'label': label}
            for value, label in ProductCategory.choices
        ],
    ]
    
    return render(
        request,
        'products/search.html',
        {
            'products': products,
            'query': query,
            'result_count': result_count,
            'categories': categories,
        }
    )
