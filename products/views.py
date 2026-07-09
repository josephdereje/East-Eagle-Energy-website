from django.shortcuts import get_object_or_404, render

from .models import Product, ProductCategory


def product_list(request, category=None):
    products = Product.objects.filter(is_active=True)
    active_category = category or 'all'

    if category and category != 'all':
        if category not in ProductCategory.values:
            category = 'all'
        else:
            products = products.filter(category=category)
            active_category = category

    categories = [
        {'slug': 'all', 'label': 'All Products'},
        *[
            {'slug': value, 'label': label}
            for value, label in ProductCategory.choices
        ],
    ]

    return render(
        request,
        'products/list.html',
        {
            'products': products,
            'categories': categories,
            'active_category': active_category,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'products/detail.html', {'product': product})
