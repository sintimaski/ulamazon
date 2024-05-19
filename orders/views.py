from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Order

from .serializers import (OrderCreateSerializer, OrderRetrieveSerializer,
                          OrderUpdateSerializer)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("items")
    # permission_classes = [IsAuthenticated]  # Assuming covered

    def get_serializer_class(self):
        if self.action in ("create",):
            return OrderCreateSerializer
        elif self.action in ("update", "partial_update"):
            return OrderUpdateSerializer
        return OrderRetrieveSerializer

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
