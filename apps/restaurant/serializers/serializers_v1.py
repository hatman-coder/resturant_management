from rest_framework import serializers
from ..models import Restaurant, Employee, Menu, MenuItem


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        exclude = ["created_at", "updated_at"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ["created_at", "updated_at"]


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        exclude = ["created_at", "updated_at"]


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        exclude = ["created_at", "updated_at"]
