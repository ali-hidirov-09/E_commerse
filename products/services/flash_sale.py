from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters, generics, serializers
from datetime import datetime, timedelta
from products.models import Product, ProductViewHistory, FlashSale
from products.filters import FlashSaleFilter
from django_filters import rest_framework as django_filter
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from products.serializers import Flashsaleserializer


class CustomPagination(PageNumberPagination):
    page_size = 3


class FlashSaleListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        qs = FlashSale.objects.all()
        current_time = now()
        qs = qs.filter(
            start_time__lte=current_time,
            end_time__gte=current_time
        )
        return qs

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = ('id', 'product', 'discount_percentage', 'start_time', 'end_time')

    pagination_class = CustomPagination
    serializer_class = FlashSaleSerializer
    filter_backends = (django_filter.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = FlashSaleFilter
    search_fields = ['product__name']


class FlashSaleListView(generics.ListAPIView):
    def get_queryset(self):
        qs = FlashSale.objects.all()
        return qs

    def get_serializer_class(self):
        sr = Flashsaleserializer
        return sr


@api_view(['GET'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()

    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=datetime.now() + timedelta(hours=24)

    ).first()

    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time
        return Response({
            "message": f"This product will be on a {discount}% of flash sale!",
            "start_time": start_time,
            "end_time": end_time
        })
    else:
        return Response({
            "message": "No upcoming flash sales for this product"
        })
