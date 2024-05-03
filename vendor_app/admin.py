"""This file defines the django official admin site to use"""
from django.contrib import admin
from .models import Vendor, PurchaseOrder

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
