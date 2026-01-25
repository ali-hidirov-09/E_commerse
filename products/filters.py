from django_filters import rest_framework as django_filters
from .models import Product, FlashSale


class Product_filter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ("category", "min_price", "max_price")


class FlashSaleFilter(django_filters.FilterSet):
    min_dis_per = django_filters.NumberFilter(field_name="discount_percentage", lookup_expr="gte")
    max_dis_per = django_filters.NumberFilter(field_name="discount_percentage", lookup_expr="lte")

    start_time = django_filters.DateTimeFilter(
        field_name="start_time",
        lookup_expr="gte"
    )
    end_time = django_filters.DateTimeFilter(
        field_name="end_time",
        lookup_expr="lte"
    )

    class Meta:
        model = FlashSale
        fields = [
            'min_dis_per',
            'max_dis_per',
            'start_time',
            'end_time',
        ]
