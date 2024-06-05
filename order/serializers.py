from rest_framework import serializers

from account.models import User
from product.models import Product
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, write_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "product", "quantity", "created_at"]
        read_only_fields = ["user", "created_at"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive number.")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(id=value.id, stock__gt=0).exists():
            raise serializers.ValidationError("Product does not exist or is out of stock.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        product = validated_data['product']
        if product.stock < validated_data['quantity']:
            raise serializers.ValidationError({"stock": ["Insufficient stock for the product."]})
        product.stock -= validated_data['quantity']
        product.save()
        return super().create(validated_data)
