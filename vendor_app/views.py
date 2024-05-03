"""This file contains vendor_app api function with required logics and token-based authentication"""
from datetime import timedelta
from django.db.models import Avg, F, ExpressionWrapper, DurationField
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer


# vendor_profile_management

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vendor(request):
    """This function creates the vendor data in the Vendor Model"""
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_vendors(request):
    """This function gives all the vendor data"""
    vendors = Vendor.objects.all().order_by('id')
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vendor(request, vendor_id):
    """This function get the vendor data with the help of vendor_id"""
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VendorSerializer(vendor)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_vendor(request, vendor_id):
    """This function updates the vendor data with the help of vendor_id"""
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VendorSerializer(vendor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vendor(request, vendor_id):
    """This function deletes the vendor data with the help of vendor_id"""
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    vendor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# purchase_order_tracking

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_purchase_order(request):
    """This function creates the purchase_order data in the PurchaseOrder Model"""
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_purchase_orders(request):
    """This function gives all the purchase_orders data"""
    purchase_orders = PurchaseOrder.objects.all().order_by('id')
    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchase_order(request, po_id):
    """This function get the purchase_order data with the help of purchase_order id"""
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PurchaseOrderSerializer(purchase_order)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_purchase_order(request, po_id):
    """This function updates the purchase_order data with the help of purchase_order id"""
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_purchase_order(request, po_id):
    """This function deletes the purchase_order data with the help of purchase_order id"""
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    purchase_order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Historical Performance Model

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vendor_performance(request, vendor_id):
    """This function gives vendor_performance with some logical calculations 
         with the help of vendor_id"""
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    completed_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status='Completed').exclude(acknowledgment_date=None)
    total_orders = completed_orders.count()

    if total_orders == 0:
        return Response({'message': 'No completed orders for this vendor'},
                                status=status.HTTP_200_OK)

    # On-Time Delivery Rate
    on_time_delivery_rate = completed_orders.filter(
        delivery_date__lte=F('acknowledgment_date')).count() / total_orders * 100

    # Quality Rating Average
    quality_rating_avg = completed_orders.aggregate(
        avg_quality=Avg('quality_rating'))['avg_quality']

    # Average Response Time
    response_times = completed_orders.annotate(response_time=ExpressionWrapper
                    (F('acknowledgment_date') - F('issue_date'), output_field=
                     DurationField())).aggregate(avg_response_time=Avg('response_time'))
    average_response_time = response_times['avg_response_time'] if response_times['avg_response_time'] else timedelta(seconds=0)

    # Fulfillment Rate
    fulfillment_rate = completed_orders.count() / total_orders * 100

    # Update Vendor performance metrics
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = average_response_time.total_seconds()  # Convert to seconds
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

    # Serialize vendor object
    serializer = VendorSerializer(vendor)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    """This function used for Acknowledge a purchase order"""
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order does not exist.'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # Update acknowledgment date
        acknowledgment_date_str = request.data.get('acknowledgment_date')
        if not acknowledgment_date_str:
            return Response({'error': 'Acknowledgment date is required in the request data.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Convert acknowledgment date string to timezone-aware datetime
        acknowledgment_date = timezone.make_aware(timezone.datetime.strptime
                            (acknowledgment_date_str, '%Y-%m-%d'))

        # Update acknowledgment date
        purchase_order.acknowledgment_date = acknowledgment_date
        purchase_order.save()

        # Recalculate average response time
        vendor = purchase_order.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor,
                            status='Completed').exclude(acknowledgment_date=None)
        response_times = completed_orders.annotate(response_time=
                        ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=
                        DurationField())).aggregate(avg_response_time=Avg('response_time'))
        average_response_time = response_times['avg_response_time'].total_seconds(
                                ) if response_times['avg_response_time'] else 0

        # Update average response time in Vendor model

        vendor.average_response_time = average_response_time
        vendor.save()

        return Response({'message': 'Purchase Order acknowledged successfully.'},
                        status=status.HTTP_200_OK)
