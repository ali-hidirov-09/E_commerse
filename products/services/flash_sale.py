from  rest_framework.decorators import api_view
from rest_framework import  generics, status, serializers
from  rest_framework.response import Response
from datetime import  timezone, datetime
from products.models import Product, FlashSale


class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = "__all__"

    serializer_class = FlashSaleSerializer

# @api_view(["GET"])

