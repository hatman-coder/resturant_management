from rest_framework import serializers
from ..models import Orders

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        exclude = ["created_at", "updated_at","is_active"]
