from rest_framework import serializers

from .models import Order, OrderItem, Product


class OrderCreateSerializer(serializers.ModelSerializer):
    purchases = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Order
        fields = ("id", "purchases", "created_at", "address", "user")

    def create(self, validated_data):
        purchases = validated_data.pop("purchases")
        errors = []

        order = Order.objects.create(**validated_data)

        for purchase in purchases:
            try:
                product = Product.objects.get(pk=purchase["id"])
                order.items.add(
                    product, through_defaults={"quantity": purchase["quantity"]}
                )

            except Product.DoesNotExist:
                errors.append(f"Product with ID {purchase["id"]} does not exist.")

        if errors:
            raise serializers.ValidationError({"error": errors})

        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    purchases = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Order
        fields = ("id", "purchases", "address", "user")
        partial = True

    def update(self, instance, validated_data):
        purchases = validated_data.pop("purchases", [])
        errors = []

        for field, value in validated_data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)

        existing_order_items = instance.items.all()
        existing_order_item_ids = [item.id for item in existing_order_items]

        for purchase in purchases:
            product_id = purchase["id"]
            quantity = purchase["quantity"]

            try:
                product = Product.objects.get(pk=product_id)
                order_item, created = OrderItem.objects.get_or_create(
                    order=instance, product=product, defaults={"quantity": quantity}
                )
                if not created:
                    order_item.quantity = quantity
                    order_item.save()
                if order_item.id in existing_order_items:
                    existing_order_item_ids.remove(order_item.id)
            except Product.DoesNotExist:
                errors.append(f"Product with ID {product_id} does not exist.")
                continue

        instance.items.filter(id__in=existing_order_item_ids).delete()
        if errors:
            raise serializers.ValidationError({"error": errors})

        instance.save()
        return instance


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
