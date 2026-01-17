from django.utils import timezone
from datetime import  timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Order, Category, Product, FlashSale
from django.contrib.auth.models import User


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Admin11", password="admin11")
        self.client.force_authenticate(user=self.user)
        self.category1 = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(name='Laptop', description='Macbook', price=1000, category=self.category1, stock=50)
        self.product2 = Product.objects.create(name='Iphone', description='Iphone 17 pro', price=1000, category=self.category1, stock=50)
        self.product3 = Product.objects.create(name='Samsung', description='Samsung s25 ultra', price=1000, category=self.category1, stock=50)
        self.order1 = Order.objects.create(
            product=self.product1,
            customer=self.user,
            quantity=2,
            phone_number="+77088613884"
        )
        self.flashsale = FlashSale.objects.create(
            product=self.product1,
            discount_percentage=15,
            start_time=timezone.now(),
            end_time = timezone.now() + timedelta(days=1)
        )
        self.order2 = Order.objects.create(
            product=self.product1,
            customer=self.user,
            quantity=2,
            phone_number="+77245613884"
        )

    def test_stock(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_authenticate(user=self.admin_user)
        initial_stock = self.product1.stock
        url = reverse('stock_replenish_stock', kwargs={
            'product_id': self.product1.id,
            'amount': 25
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, initial_stock + 25)


    def test_all_sales(self):
        url = reverse('sales_all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)


    def test_sale_post(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('sale')
        data = {
            "product": self.product3.id,
            "discount_percentage": 25,
            "start_time":timezone.now().isoformat(),
            "end_time": (timezone.now() + timedelta(days=1)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_product_view(self):
        url=reverse('product-view-history-create')
        data = {
            "user": self.user.id,
            "product": self.product1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_check_sale(self):
        url = reverse('check_sale', kwargs={'product_id': self.product1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_check_sale_not_found(self):
        url = reverse('check_sale', kwargs={'product_id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

