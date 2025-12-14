from time import timezone

from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    content= models.TextField()  # yozish
    rating = models.PositiveIntegerField() # ball berish
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.rating}"


class FlashSale(models.Model):
    """Vaqtinchalik skidka, 2-3 kunlik skidka, odamga qiziq bo'lgan rekomendasiya faqat shu odamga ko'rinadi, agar odam bir marta shu maxsulotni ko'rsa uni shu odamga skidka bo'lganda jo'natadi, ko'rsatadi"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    class Meta:
        """Bazada uchalssi bir xil bo'lgan
         ma'lumot qo'shomisiz"""
        unique_together = ("product", 'start_time', 'end_time')
