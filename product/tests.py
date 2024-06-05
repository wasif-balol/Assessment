from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from account.models import User
from product.models import Product


class ProductTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='password',
            first_name='Admin',
            last_name='User'
        )
        self.client.force_authenticate(user=self.admin_user)
        self.product_url = reverse('product-list')
        self.product_detail_url = lambda pk: reverse('product-detail', args=[pk])

    def test_create_product(self):
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 10.00,
            'stock': 100
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.get()
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.price, data['price'])
        self.assertEqual(product.stock, data['stock'])

    def test_create_product_invalid_price(self):
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': -10.00,
            'stock': 100
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_create_product_invalid_stock(self):
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 10.00,
            'stock': -5
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stock', response.data)

    def test_list_products(self):
        Product.objects.create(name='Test Product', description='Test Description', price=10.00, stock=100)
        response = self.client.get(self.product_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Product')
        self.assertEqual(response.data[0]['description'], 'Test Description')
        self.assertEqual(float(response.data[0]['price']), 10.00)
        self.assertEqual(response.data[0]['stock'], 100)

    def test_update_product(self):
        product = Product.objects.create(name='Test Product', description='Test Description', price=10.00, stock=100)
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 20.00,
            'stock': 50
        }
        response = self.client.put(self.product_detail_url(product.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.price, data['price'])
        self.assertEqual(product.stock, data['stock'])

    def test_delete_product(self):
        product = Product.objects.create(name='Test Product', description='Test Description', price=10.00, stock=100)
        response = self.client.delete(self.product_detail_url(product.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
