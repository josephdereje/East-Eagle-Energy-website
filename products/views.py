import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import Truncator

from .models import (
    EssSubType,
    Product,
    ProductCategory,
    ProductSidebarSection,
    ProductType,
    RecommendedProduct,
    VoltageType,
)

PRODUCTS_PER_PAGE = 12

def _product_card_payload(product):
    desc = product.short_description or strip_tags(product.description or '')
    type_labels = {
        ProductType.INVERTER: 'Inverter',
        ProductType.SOLAR_PANEL: 'Solar Panel',
        ProductType.EV_CHARGER: 'EV Charger',
        ProductType.ENERGY_STORAGE: 'ESS',
    }
    icon = 'fa-solar-panel' if product.product_type == ProductType.INVERTER else 'fa-battery-full'
    if product.product_type == ProductType.SOLAR_PANEL:
        icon = 'fa-solar-panel'
    elif product.product_type == ProductType.EV_CHARGER:
        icon = 'fa-charging-station'

    return {
        'name': product.name,
        'slug': product.slug,
        'url': product.get_absolute_url(),
        'image_url': product.image.url if product.image else '',
        'short_description': Truncator(desc).words(12, truncate=' …'),
        'product_type': product.product_type,
        'type_label': type_labels.get(product.product_type, 'ESS'),
        'type_class': {
            ProductType.INVERTER: 'dyness-tag--inverter',
            ProductType.SOLAR_PANEL: 'dyness-tag--solar',
            ProductType.EV_CHARGER: 'dyness-tag--ev',
        }.get(product.product_type, 'dyness-tag--ess'),
        'voltage_label': (
            product.voltage_label
            if product.voltage_type != VoltageType.NOT_APPLICABLE
            else ''
        ),
        'ess_sub_type_label': (
            product.ess_sub_type_label
            if product.ess_sub_type != EssSubType.NOT_APPLICABLE
            else ''
        ),
        'icon': icon,
    }


def _wants_ajax(request):
    return (
        request.GET.get('ajax') == '1'
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    )


def _product_count(**filters):
    return Product.objects.filter(is_active=True, **filters).count()


def build_product_nav(section='ess'):
    """Build Dyness-style sidebar navigation with live product counts."""
    if section == 'ess':
        return [
            {
                'title': 'Residential Energy Storage Systems',
                'icon': 'fa-house',
                'items': [
                    {
                        'label': 'Low Voltage ESS',
                        'url': reverse('products:ess_residential_voltage', kwargs={'voltage_type': 'low-voltage'}),
                        'filter_key': 'low_voltage',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.ENERGY_STORAGE,
                            category=ProductCategory.RESIDENTIAL,
                            voltage_type=VoltageType.LOW_VOLTAGE,
                        ),
                    },
                    {
                        'label': 'High Voltage ESS',
                        'url': reverse('products:ess_residential_voltage', kwargs={'voltage_type': 'high-voltage'}),
                        'filter_key': 'high_voltage',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.ENERGY_STORAGE,
                            category=ProductCategory.RESIDENTIAL,
                            voltage_type=VoltageType.HIGH_VOLTAGE,
                        ),
                    },
                ],
            },
            {
                'title': 'C & I Energy Storage Systems',
                'icon': 'fa-industry',
                'items': [
                    {
                        'label': 'Stacked ESS',
                        'url': reverse('products:ess_ci_subtype', kwargs={'ess_sub_type': 'stacked'}),
                        'filter_key': 'stacked_ess',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.ENERGY_STORAGE,
                            category=ProductCategory.C_AND_I_BESS,
                            ess_sub_type=EssSubType.STACKED_ESS,
                        ),
                    },
                    {
                        'label': 'All-in-One ESS',
                        'url': reverse('products:ess_ci_subtype', kwargs={'ess_sub_type': 'all-in-one'}),
                        'filter_key': 'all_in_one_ess',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.ENERGY_STORAGE,
                            category=ProductCategory.C_AND_I_BESS,
                            ess_sub_type=EssSubType.ALL_IN_ONE_ESS,
                        ),
                    },
                    {
                        'label': 'Storage & Charging',
                        'url': reverse('products:ess_ci_subtype', kwargs={'ess_sub_type': 'storage-charging'}),
                        'filter_key': 'storage_charging',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.ENERGY_STORAGE,
                            category=ProductCategory.C_AND_I_BESS,
                            ess_sub_type=EssSubType.STORAGE_CHARGING,
                        ),
                    },
                ],
            },
            {
                'title': 'ESS Solutions',
                'icon': 'fa-bolt',
                'items': [
                    {
                        'label': 'All ESS Solutions',
                        'url': reverse('products:ess_solutions'),
                        'filter_key': 'ess_solution',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.ENERGY_STORAGE,
                            category=ProductCategory.ESS_SOLUTION,
                        ),
                    },
                ],
            },
            {
                'title': 'Smart Energy Management System',
                'icon': 'fa-chart-line',
                'items': [
                    {
                        'label': 'All Smart Energy Systems',
                        'url': reverse('products:ess_smart_energy'),
                        'filter_key': 'smart_energy_management',
                        'is_sub': False,
                        'count': _product_count(
                            ess_sub_type=EssSubType.SMART_ENERGY_MANAGEMENT,
                        ),
                    },
                    {
                        'label': 'Cloud Monitoring',
                        'url': reverse('products:ess_cloud_monitoring'),
                        'filter_key': 'cloud_monitoring',
                        'is_sub': True,
                        'count': _product_count(
                            ess_sub_type=EssSubType.CLOUD_MONITORING,
                        ),
                    },
                ],
            },
        ]

    if section == 'inverters':
        return [
            {
                'title': 'Residential Inverters',
                'icon': 'fa-house',
                'items': [
                    {
                        'label': 'Hybrid Inverters',
                        'url': reverse('products:inverter_category', kwargs={'category': 'residential'}),
                        'filter_key': 'residential_inverter',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.INVERTER,
                            category=ProductCategory.RESIDENTIAL,
                        ),
                    },
                ],
            },
            {
                'title': 'C & I Inverters',
                'icon': 'fa-industry',
                'items': [
                    {
                        'label': 'Commercial Inverters',
                        'url': reverse('products:inverter_category', kwargs={'category': 'c-and-i-bess'}),
                        'filter_key': 'c_and_i_inverter',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.INVERTER,
                            category=ProductCategory.C_AND_I_BESS,
                        ),
                    },
                ],
            },
            {
                'title': 'All Inverters',
                'icon': 'fa-plug',
                'items': [
                    {
                        'label': 'View All Inverters',
                        'url': reverse('products:inverters'),
                        'filter_key': 'all_inverters',
                        'is_sub': False,
                        'count': _product_count(product_type=ProductType.INVERTER),
                    },
                ],
            },
        ]

    if section == 'solar_panels':
        return [
            {
                'title': 'Solar Panel Products',
                'icon': 'fa-solar-panel',
                'items': [
                    {
                        'label': 'All Solar Panels',
                        'url': reverse('products:solar_panels'),
                        'filter_key': 'all_solar_panels',
                        'is_sub': False,
                        'count': _product_count(product_type=ProductType.SOLAR_PANEL),
                    },
                    {
                        'label': 'Residential Solar Panels',
                        'url': reverse('products:solar_panel_category', kwargs={'category': 'residential'}),
                        'filter_key': 'residential_solar_panel',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.SOLAR_PANEL,
                            category=ProductCategory.RESIDENTIAL,
                        ),
                    },
                    {
                        'label': 'C & I Solar Panels',
                        'url': reverse('products:solar_panel_category', kwargs={'category': 'c-and-i-bess'}),
                        'filter_key': 'c_and_i_solar_panel',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.SOLAR_PANEL,
                            category=ProductCategory.C_AND_I_BESS,
                        ),
                    },
                ],
            },
        ]

    if section == 'ev_chargers':
        return [
            {
                'title': 'EV Charger Products',
                'icon': 'fa-charging-station',
                'items': [
                    {
                        'label': 'All EV Chargers',
                        'url': reverse('products:ev_chargers'),
                        'filter_key': 'all_ev_chargers',
                        'is_sub': False,
                        'count': _product_count(product_type=ProductType.EV_CHARGER),
                    },
                    {
                        'label': 'Residential EV Chargers',
                        'url': reverse('products:ev_charger_category', kwargs={'category': 'residential'}),
                        'filter_key': 'residential_ev_charger',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.EV_CHARGER,
                            category=ProductCategory.RESIDENTIAL,
                        ),
                    },
                    {
                        'label': 'C & I EV Chargers',
                        'url': reverse('products:ev_charger_category', kwargs={'category': 'c-and-i-bess'}),
                        'filter_key': 'c_and_i_ev_charger',
                        'is_sub': False,
                        'count': _product_count(
                            product_type=ProductType.EV_CHARGER,
                            category=ProductCategory.C_AND_I_BESS,
                        ),
                    },
                ],
            },
        ]

    return []


def _get_page_title(section, category=None, voltage_type=None, ess_sub_type=None, product_type_filter=None):
    titles = {
        EssSubType.STACKED_ESS: 'Stacked ESS',
        EssSubType.ALL_IN_ONE_ESS: 'All-in-One ESS',
        EssSubType.STORAGE_CHARGING: 'Storage & Charging',
        EssSubType.SMART_ENERGY_MANAGEMENT: 'Smart Energy Management System',
        EssSubType.CLOUD_MONITORING: 'Cloud Monitoring',
    }
    if ess_sub_type in titles:
        return titles[ess_sub_type]

    if section == 'solar_panels' or product_type_filter == ProductType.SOLAR_PANEL:
        if category == ProductCategory.RESIDENTIAL:
            return 'Residential Solar Panels'
        if category == ProductCategory.C_AND_I_BESS:
            return 'C & I Solar Panels'
        return 'Solar Panels'
    if section == 'ev_chargers' or product_type_filter == ProductType.EV_CHARGER:
        if category == ProductCategory.RESIDENTIAL:
            return 'Residential EV Chargers'
        if category == ProductCategory.C_AND_I_BESS:
            return 'C & I EV Chargers'
        return 'EV Chargers'

    if section == 'inverters':
        if category == ProductCategory.RESIDENTIAL:
            return 'Residential Inverters'
        if category == ProductCategory.C_AND_I_BESS:
            return 'C & I Inverters'
        return 'Inverters'

    if category == ProductCategory.ESS_SOLUTION:
        return 'ESS Solutions'
    if category == ProductCategory.C_AND_I_BESS:
        return 'C & I Energy Storage Systems'
    if category == ProductCategory.RESIDENTIAL:
        if voltage_type == VoltageType.LOW_VOLTAGE:
            return 'Low Voltage ESS'
        if voltage_type == VoltageType.HIGH_VOLTAGE:
            return 'High Voltage ESS'
        return 'Residential Energy Storage Systems'
    return 'Energy Storage Systems'


def product_list(
    request,
    section='ess',
    category=None,
    voltage_type=None,
    ess_sub_type=None,
    product_type_filter=None,
):
    products = Product.objects.filter(is_active=True)
    active_section = section
    active_category = category or 'all'
    active_voltage = voltage_type or 'all'
    active_ess_sub = ess_sub_type or 'all'
    active_product_type = product_type_filter or 'all'
    sidebar_section = None

    if section == 'inverters':
        products = products.filter(product_type=ProductType.INVERTER)
    elif section == 'solar_panels':
        products = products.filter(product_type=ProductType.SOLAR_PANEL)
    elif section == 'ev_chargers':
        products = products.filter(product_type=ProductType.EV_CHARGER)
    else:
        products = products.filter(
            Q(product_type=ProductType.ENERGY_STORAGE)
            | Q(ess_sub_type__in=[
                EssSubType.SMART_ENERGY_MANAGEMENT,
                EssSubType.CLOUD_MONITORING,
            ])
        )
        section = 'ess'

    category_map = {
        'residential': ProductCategory.RESIDENTIAL,
        'c-and-i-bess': ProductCategory.C_AND_I_BESS,
        'c_and_i_bess': ProductCategory.C_AND_I_BESS,
        'ess-solution': ProductCategory.ESS_SOLUTION,
        'ess_solution': ProductCategory.ESS_SOLUTION,
    }
    if category:
        db_category = category_map.get(category, category)
        if db_category in ProductCategory.values:
            products = products.filter(category=db_category)
            active_category = db_category
            try:
                sidebar_section = ProductSidebarSection.objects.get(
                    category=db_category,
                    is_active=True,
                )
            except ProductSidebarSection.DoesNotExist:
                pass

    voltage_map = {
        'low-voltage': VoltageType.LOW_VOLTAGE,
        'high-voltage': VoltageType.HIGH_VOLTAGE,
    }
    if voltage_type:
        db_voltage = voltage_map.get(voltage_type, voltage_type)
        if db_voltage in VoltageType.values:
            products = products.filter(voltage_type=db_voltage)
            active_voltage = db_voltage

    ess_map = {
        'stacked': EssSubType.STACKED_ESS,
        'all-in-one': EssSubType.ALL_IN_ONE_ESS,
        'storage-charging': EssSubType.STORAGE_CHARGING,
        'smart-energy': EssSubType.SMART_ENERGY_MANAGEMENT,
        'cloud-monitoring': EssSubType.CLOUD_MONITORING,
    }
    if ess_sub_type:
        db_ess = ess_map.get(ess_sub_type, ess_sub_type)
        if db_ess in EssSubType.values:
            products = products.filter(ess_sub_type=db_ess)
            active_ess_sub = db_ess

    type_map = {'inverter': ProductType.INVERTER}
    if product_type_filter:
        db_type = type_map.get(product_type_filter, product_type_filter)
        if db_type in ProductType.values:
            products = products.filter(product_type=db_type)
            active_product_type = db_type

    page_title = _get_page_title(
        section, active_category, active_voltage, active_ess_sub, active_product_type,
    )
    nav_groups = build_product_nav(section)

    active_filter = 'all'
    if section == 'solar_panels':
        if active_category == ProductCategory.RESIDENTIAL:
            active_filter = 'residential_solar_panel'
        elif active_category == ProductCategory.C_AND_I_BESS:
            active_filter = 'c_and_i_solar_panel'
        else:
            active_filter = 'all_solar_panels'
    elif section == 'ev_chargers':
        if active_category == ProductCategory.RESIDENTIAL:
            active_filter = 'residential_ev_charger'
        elif active_category == ProductCategory.C_AND_I_BESS:
            active_filter = 'c_and_i_ev_charger'
        else:
            active_filter = 'all_ev_chargers'
    elif active_product_type != 'all':
        active_filter = active_product_type
    elif active_ess_sub != 'all':
        active_filter = active_ess_sub
    elif active_category == ProductCategory.ESS_SOLUTION:
        active_filter = 'ess_solution'
    elif active_voltage != 'all':
        active_filter = active_voltage
    elif active_category == ProductCategory.RESIDENTIAL and section == 'inverters':
        active_filter = 'residential_inverter'
    elif active_category == ProductCategory.C_AND_I_BESS and section == 'inverters':
        active_filter = 'c_and_i_inverter'
    elif section == 'inverters' and active_category == 'all' and active_product_type == 'all':
        active_filter = 'all_inverters'

    seo_title = f'{page_title} | East Eagle Energy'
    seo_description = (
        f'Browse East Eagle Energy {page_title} — solar inverters, batteries, '
        f'EV chargers, and energy storage systems worldwide.'
    )

    schema = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': seo_title,
        'url': 'https://www.easteagleenergy.com/products/',
        'numberOfItems': products.count(),
    }

    recommended = (
        RecommendedProduct.objects.filter(is_active=True)
        .select_related('product')
        .order_by('display_order', '-created_at')[:12]
    )

    products = products.order_by('name')
    total_products = products.count()
    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    schema['numberOfItems'] = total_products

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'total_products': total_products,
        'nav_groups': nav_groups,
        'active_section': active_section,
        'active_category': active_category,
        'active_voltage': active_voltage,
        'active_ess_sub': active_ess_sub,
        'active_filter': active_filter,
        'page_title': page_title,
        'sidebar_section': sidebar_section,
        'recommended_products': recommended,
        'seo_title': seo_title,
        'seo_description': seo_description,
        'seo_keywords': (
            'solar inverter, solar panel, EV charger, battery storage, BESS, ESS, '
            'energy storage, East Eagle Energy products'
        ),
        'schema_json': json.dumps(schema),
    }

    if _wants_ajax(request):
        return JsonResponse({
            'ok': True,
            'page_title': page_title,
            'seo_title': seo_title,
            'active_section': active_section,
            'active_filter': active_filter,
            'total_products': total_products,
            'nav_groups': nav_groups,
            'products': [_product_card_payload(p) for p in page_obj.object_list],
            'pagination': {
                'page': page_obj.number,
                'num_pages': paginator.num_pages,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'page_range': list(paginator.page_range),
                'showing': len(page_obj.object_list),
            },
        })

    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('gallery_images'),
        slug=slug,
        is_active=True,
    )
    gallery_images = product.get_gallery_items()

    sidebar_section = None
    try:
        sidebar_section = ProductSidebarSection.objects.get(
            category=product.category,
            is_active=True,
        )
    except ProductSidebarSection.DoesNotExist:
        pass

    related_products = Product.objects.filter(
        product_type=product.product_type,
        is_active=True,
    ).exclude(id=product.id)[:4]

    if gallery_images:
        og_image = f'https://www.easteagleenergy.com{gallery_images[0]["url"]}'
    elif product.image:
        og_image = f'https://www.easteagleenergy.com{product.image.url}'
    else:
        og_image = 'https://www.easteagleenergy.com/images/logo.png'
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': product.name,
        'description': product.short_description or product.description[:160],
        'brand': {'@type': 'Brand', 'name': 'East Eagle Energy'},
        'url': f'https://www.easteagleenergy.com{product.get_absolute_url()}',
        'image': [f'https://www.easteagleenergy.com{item["url"]}' for item in gallery_images]
        if len(gallery_images) > 1 else og_image,
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
            'gallery_images': gallery_images,
            'related_products': related_products,
            'sidebar_section': sidebar_section,
            'seo_title': f'{product.name} | East Eagle Energy',
            'seo_description': product.short_description or product.description[:160],
            'og_image': og_image,
            'og_type': 'product',
            'schema_json': json.dumps(schema),
        },
    )


def product_search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(category__icontains=query)
            | Q(product_type__icontains=query)
        )

    result_count = products.count()

    browse_links = [
        {'label': 'Energy Storage Systems', 'url_name': 'products:ess'},
        {'label': 'Residential ESS', 'url_name': 'products:ess_residential'},
        {'label': 'C & I Energy Storage', 'url_name': 'products:ess_ci'},
        {'label': 'Smart Energy Management', 'url_name': 'products:ess_smart_energy'},
        {'label': 'Solar Panels', 'url_name': 'products:solar_panels'},
        {'label': 'EV Chargers', 'url_name': 'products:ev_chargers'},
        {'label': 'Inverters & Equipment', 'url_name': 'products:inverters'},
    ]

    return render(
        request,
        'products/search.html',
        {
            'products': products,
            'query': query,
            'result_count': result_count,
            'browse_links': browse_links,
        },
    )
