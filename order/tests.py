from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from account.models import User
from product.models import Product
from .models import Order


class OrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', first_name='Test',
                                             last_name='User')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                              stock=100)
        self.order_url = reverse('order-list-create')

    def test_create_order(self):
        data = {'product': self.product.id, 'quantity': 1}
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().user, self.user)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 99)

    def test_create_order_invalid_quantity(self):
        data = {'product': self.product.id, 'quantity': -1}
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_insufficient_stock(self):
        data = {'product': self.product.id, 'quantity': 101}
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders(self):
        Order.objects.create(user=self.user, product=self.product, quantity=1)
        response = self.client.get(self.order_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_permission(self):
        other_user = User.objects.create_user(username='otheruser', password='password', first_name='Other',
                                              last_name='User')
        Order.objects.create(user=other_user, product=self.product, quantity=1)
        response = self.client.get(self.order_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
