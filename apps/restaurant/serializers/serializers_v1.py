from rest_framework import serializers
from ..models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        exclude = ["created_at", "updated_at"]


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        exclude = ["created_at", "updated_at"]
