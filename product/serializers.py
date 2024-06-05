from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "created_at"]
        read_only_fields = ["created_at"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
