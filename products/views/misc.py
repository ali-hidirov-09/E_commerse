from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializers, ReviewSerializers, CategorySerializer
from .models import Product, Category, Review
from django.db import  models
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .filters import Product_filter
from django_filters import rest_framework as dr
from rest_framework.permissions import IsAuthenticated


class CustomPagination(PageNumberPagination):
    page_size = 5

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] # default = AllowAny

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

