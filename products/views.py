from .serializers import ProductSerializers, ReviewSerializers, CategorySerializer, CustomerSerializer
from .models import Product, Category, Review, Customer
from django.db import  models
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def list(self, request, *args, **kwargs):
        """xammasini get qilish. list degani biz ozida bor funksiyani foydalanyapmiz"""
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        """Bu faqat bittasini get qilganda, va  biz buni xam ozgartiramiz aslida esa bu bor edi"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializers(related_products, many=True)
        return Response({
            "product":serializer.data,
            "ralated_products":related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:3]
        serializer = ProductSerializers(top_products, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        """ o'rtacha reytinngni chiqaradigan kod"""
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({"avarage_rating": "No reviews yet! "})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()
        return Response({"average_rating": avg_rating})
