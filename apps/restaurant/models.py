from django.db import models
from abstract.base_model import BaseModel
from apps.user.models import User


class Restaurant(BaseModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="restaurant_owner"
    )
    name = models.CharField(max_length=252)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class Employee(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="restaurant_employee"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="employee_restaurant"
    )
    salary = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.restaurant.name})"


class Menu(BaseModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class MenuItem(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.menu.name})"
