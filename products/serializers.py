from rest_framework import serializers
from .models import Product, Category, Review, ProductViewHistory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProductSerializers(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True, required=False)
    class Meta:
        model = Product
        fields = ["id", "name","category","price", "description", "avg_rating"]



class ProductViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViewHistory
        fields = '__all__'