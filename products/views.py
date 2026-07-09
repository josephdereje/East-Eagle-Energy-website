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
    
    return render(
        request, 
        'products/detail.html', 
        {
            'product': product,
            'related_products': related_products,
            'sidebar_section': sidebar_section,
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
