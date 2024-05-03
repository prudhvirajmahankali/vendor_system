"""Serializer for Vendor model"""
from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for Vendor model"""
    class Meta:
        """Meta class defining metadata for VendorSerializer"""
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address',
                  'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 
                  'average_response_time', 'fulfillment_rate']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseOrder model"""
    class Meta:
        """Meta class defining metadata for PurchaseOrderSerializer"""
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items',
                  'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
