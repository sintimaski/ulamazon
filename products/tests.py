from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product1 = Product.objects.create(
            name="Product 1", price=10.0, user=self.user
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=20.0, user=self.user
        )
        for i in range(5, 15):
            Product.objects.create(name=f"Product {i}", price=20.0, user=self.user)
        self.total_products = 12

    def test_list_products(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], self.total_products)

    def test_list_products_empty(self):
        Product.objects.all().delete()
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_retrieve_product(self):
        url = reverse("product-detail", args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Product 1")
        self.assertEqual(float(response.data["price"]), 10.0)

    def test_retrieve_product_invalid(self):
        url = reverse("product-detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_products_with_pagination(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)

    def test_list_products_with_filtering(self):
        url = reverse("product-list")
        url = url + f"?name={self.product2.name}"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Product 2")
        self.assertEqual(float(response.data["results"][0]["price"]), 20.0)
