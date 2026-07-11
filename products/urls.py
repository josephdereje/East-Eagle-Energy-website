from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('search/', views.product_search, name='search'),

    # Energy Storage Systems (ESS)
    path('ess/', views.product_list, {'section': 'ess'}, name='ess'),
    path('ess/residential/', views.product_list, {
        'section': 'ess', 'category': 'residential',
    }, name='ess_residential'),
    path('ess/residential/<slug:voltage_type>/', views.product_list, {
        'section': 'ess', 'category': 'residential',
    }, name='ess_residential_voltage'),
    path('ess/c-and-i-bess/', views.product_list, {
        'section': 'ess', 'category': 'c-and-i-bess',
    }, name='ess_ci'),
    path('ess/c-and-i-bess/<slug:ess_sub_type>/', views.product_list, {
        'section': 'ess', 'category': 'c-and-i-bess',
    }, name='ess_ci_subtype'),
    path('ess/solutions/', views.product_list, {
        'section': 'ess', 'category': 'ess-solution',
    }, name='ess_solutions'),
    path('ess/smart-energy/', views.product_list, {
        'section': 'ess', 'ess_sub_type': 'smart-energy',
    }, name='ess_smart_energy'),
    path('ess/smart-energy/cloud-monitoring/', views.product_list, {
        'section': 'ess', 'ess_sub_type': 'cloud-monitoring',
    }, name='ess_cloud_monitoring'),

    # Inverters
    path('inverters/', views.product_list, {'section': 'inverters'}, name='inverters'),
    path('inverters/<slug:category>/', views.product_list, {
        'section': 'inverters',
    }, name='inverter_category'),

    # Solar Panels
    path('solar-panels/', views.product_list, {
        'section': 'solar_panels',
    }, name='solar_panels'),
    path('solar-panels/<slug:category>/', views.product_list, {
        'section': 'solar_panels',
    }, name='solar_panel_category'),

    # EV Chargers
    path('ev-chargers/', views.product_list, {
        'section': 'ev_chargers',
    }, name='ev_chargers'),
    path('ev-chargers/<slug:category>/', views.product_list, {
        'section': 'ev_chargers',
    }, name='ev_charger_category'),

    # Legacy category URLs
    path('category/<slug:category>/', views.product_list, name='category'),
    path('category/<slug:category>/<slug:voltage_type>/', views.product_list, name='category_voltage'),

    path('<slug:slug>/', views.product_detail, name='detail'),
]
