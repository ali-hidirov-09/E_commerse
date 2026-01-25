from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Order, Category, Product
from django.contrib.auth.models import User


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Admin11", password="admin11")
        self.client.force_authenticate(user=self.user)
        self.category1 = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(name='Laptop', description='Macbook', price=1000,
                                               category=self.category1, stock=50)
        self.order1 = Order.objects.create(
            product=self.product1,
            customer=self.user,
            quantity=2,
            phone_number="+77088613884"
        )
        self.order2 = Order.objects.create(
            product=self.product1,
            customer=self.user,
            quantity=2,
            phone_number="+77245613884"
        )

    def test_order_list(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_order_detail(self):
        url = reverse('order-detail', args={self.order1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_order_create(self):
        url = reverse('order-list')
        data = {
            'product': self.product1.id,
            'customer': self.user.id,
            'quantity': 3,
            'phone_number': '+77088613884'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_order_update(self):
        url = reverse('order-detail', args={self.order2.id})
        data = {
            'product': self.product1.id,
            'customer': self.user.id,
            'quantity': 3,
            'phone_number': '+77088613884',
            'is_paid': 'true'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_category_delete(self):
        url = reverse('order-detail', args={self.order2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
