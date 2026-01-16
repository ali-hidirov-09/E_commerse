from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from products.models import Product, Category, Review, User


class ProductViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user1",email="test_user1@gmail.com", password="test_user_01")
        self.staff_user = User.objects.create_user(username="test_user2",email="test_user2@gmail.com", password="test_user_02",is_staff=True )
        self.admin_user = User.objects.create_superuser(username="admin",email="admin@gmail.com",password="admin_123")

        self.category_1 = Category.objects.create(name="Phone")
        self.category_2 = Category.objects.create(name="Books")

        self.product_1 = Product.objects.create(name='Iphone', description="Iphone 17 pro max", category=self.category_1, price=5000)
        self.product_2 = Product.objects.create(name='Book', description="Xamsa asari ", category=self.category_2, price=2000)

        Review.objects.create(product=self.product_1, rating=5,user_id=1)
        Review.objects.create(product=self.product_1, rating=3,user_id=2)
        Review.objects.create(product=self.product_2, rating=1,user_id=2)

    def test_product_list(self):
        url = reverse('product-list')
        self.client.force_authenticate(self.user)   #majbutiy auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # request responcesi 200 ga tengmi tekshiradi


    def test_product_filter_by_category(self):
        url = reverse('product-list')+ '?category='+ str(self.category_1.id)
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


    def test_product_detail(self):
        url = reverse('product-detail', args=[self.product_1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product']['name'], 'Iphone')



    def test_top_rated(self):
        url = reverse('product-top-rated')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Iphone')

    def test_average_rated(self):
        url = reverse('product-average-rating', args=[self.product_1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 4.0)


    def test_permission_denied_for_anonymous_create(self):
        self.client.force_authenticate(user=None)
        url = reverse('product-list')
        data = {'name': 'Test product', 'description': 'This is a test product', 'price': 10.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_permission_granted_for_staff(self):
        url = reverse('product-list')
        self.client.force_authenticate(self.staff_user)
        data = {'name': 'Test product', 'description': 'This is a test product', 'price': 10.00}
        response = self.client.post(url, data,format='json' )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)















