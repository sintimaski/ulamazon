from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Order, Product


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product1 = Product.objects.create(name="Product 1", price=10.0, user=self.user)
        self.product2 = Product.objects.create(name="Product 2", price=20.0, user=self.user)

        self.order1 = Order.objects.create(user=self.user, address="address1")
        self.order2 = Order.objects.create(user=self.user, address="address2")

    def test_create_order(self):
        data = {
            "user": self.user.id,
            "address": "address3",
            "purchases": [
                {"id": self.product1.id, "quantity": 5},
                {"id": self.product2.id, "quantity": 10},
            ],
        }
        url = reverse("order-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)

        data = response.json()
        new_id = data["id"]
        order = Order.objects.get(pk=new_id)

        order_items = order.order_items
        self.assertEqual(order_items.count(), 2)
        self.assertEqual(order_items.first().quantity, 5)

    def test_create_order_invalid(self):
        data = {
            "user": self.user.id,
            "address": "address3",
            "purchases": [
                {"id": self.product1.id, "quantity": 5},
                {"id": 999, "quantity": 10},
            ],
        }
        url = reverse("order-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["error"][0], "Product with ID 999 does not exist."
        )
        self.assertEqual(Order.objects.count(), 3)

    def test_list_orders(self):
        response = self.client.get(reverse("order-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_order(self):
        data = {
            "address": "address2change",
            "purchases": [
                {"id": self.product1.id, "quantity": 3},
                {"id": self.product2.id, "quantity": 1},
            ],
        }
        url = reverse("order-detail", args=[self.order1.id])
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order1.refresh_from_db()
        self.assertEqual(self.order1.address, "address2change")

        order_items = self.order1.order_items
        self.assertEqual(order_items.count(), 2)
        self.assertEqual(order_items.first().quantity, 3)

    def test_update_order_invalid(self):
        data = {
            "user": self.user.id,
            "address": "address2change",
            "purchases": [
                {"id": self.product1.id, "quantity": 3},
                {"id": 999, "quantity": 1},
            ],
        }
        url = reverse("order-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["error"][0], "Product with ID 999 does not exist."
        )
        self.assertEqual(Order.objects.count(), 3)
