"""Models for Vendor Management System"""
from django.db import models

class Vendor(models.Model):
    """Model representing a vendor.

    Attributes:
        name (str): The name of the vendor.
        contact_details (str): Contact information of the vendor.
        address (str): Physical address of the vendor.
        vendor_code (str): A unique identifier for the vendor.
        on_time_delivery_rate (float): Percentage of orders delivered by the promised date.
        quality_rating_avg (float): Average rating of quality based on purchase orders.
        average_response_time (float): Average time taken by the vendor to respond to 
                                       purchase orders.
        fulfillment_rate (float): Percentage of purchase orders fulfilled without issues.
    """
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)


class PurchaseOrder(models.Model):
    """Model representing a purchase order.

    Attributes:
        po_number (str): Unique number identifying the purchase order.
        vendor (Vendor): The vendor associated with the purchase order.
        order_date (DateTime): Date when the purchase order was placed.
        delivery_date (DateTime): Expected or actual delivery date of the purchase order.
        items (dict): Details of items ordered.
        quantity (int): Total quantity of items in the purchase order.
        status (str): Current status of the purchase order.
        quality_rating (float): Rating given to the vendor for this purchase order.
        issue_date (DateTime): Timestamp when the purchase order was issued.
              acknowledgment_date (DateTime, optional): Timestamp when the vendor 
        acknowledged the purchase order.
    """
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.po_number)


class HistoricalPerformance(models.Model):
    """Model representing historical performance metrics of a vendor.

    Attributes:
        vendor (Vendor): The vendor associated with the historical performance metrics.
        date (DateTime): Date of the performance record.
        on_time_delivery_rate (float): Historical record of the on-time delivery rate.
        quality_rating_avg (float): Historical record of the average quality rating.
        average_response_time (float): Historical record of the average response time.
        fulfillment_rate (float): Historical record of the fulfillment rate.
    """
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='historical_performance')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return f"{self.vendor.name}'s Historical Performance"
