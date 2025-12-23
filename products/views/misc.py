from rest_framework.pagination import PageNumberPagination
from products.serializers import *
from products.models import *
from products.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class CustomPagination(PageNumberPagination):
    page_size = 5

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly] # default = AllowAny

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

