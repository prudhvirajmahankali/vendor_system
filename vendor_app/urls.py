"""URL configuration for vendor_app"""
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('api/token/', obtain_auth_token, name='api_token'),
    path('POST/api/vendors/', views.create_vendor, name='create_vendor'),
    path('GET/api/vendors/', views.list_vendors, name='list_vendors'),
    path('GET/api/vendors/<int:vendor_id>/', views.get_vendor, name='get_vendor'),
    path('PUT/api/vendors/<int:vendor_id>/', views.update_vendor, name='update_vendor'),
    path('DELETE/api/vendors/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),
    path('POST/api/purchase_orders/', views.create_purchase_order, name='create_purchase_order'),
    path('GET/api/purchase_orders/', views.list_purchase_orders, name='list_purchase_orders'),
    path('GET/api/purchase_orders/<int:po_id>/',
                       views.get_purchase_order, name='get_purchase_order'),
    path('PUT/api/purchase_orders/<int:po_id>/',
                       views.update_purchase_order, name='update_purchase_order'),
    path('DELETE/api/purchase_orders/<int:po_id>/',
                       views.delete_purchase_order, name='delete_purchase_order'),
    path('GET/api/vendors/<int:vendor_id>/performance/',
                       views.get_vendor_performance, name='get_vendor_performance'),
    path('POST/api/purchase_orders/<int:po_id>/acknowledge/',
                       views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
]
