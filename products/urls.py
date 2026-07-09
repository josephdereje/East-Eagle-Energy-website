from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('search/', views.product_search, name='search'),
    path('category/<slug:category>/', views.product_list, name='category'),
    path('category/<slug:category>/<slug:voltage_type>/', views.product_list, name='category_voltage'),
    path('<slug:slug>/', views.product_detail, name='detail'),
]
