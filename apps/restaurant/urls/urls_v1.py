from django.urls import path, include
from apps.restaurant.views.views_v1 import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("restaurant", RestaurantViewSet, basename="restaurant")
router.register("menu", MenuViewSet, basename="menu")
router.register("menu_item", MenuItemViewSet, basename="menu_item")
router.register("employee", EmployeeViewSet, basename="employee")

urlpatterns = [path(r"", include(router.urls))]
