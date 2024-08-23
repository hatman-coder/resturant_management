from rest_framework.viewsets import ModelViewSet
from ..models import Restaurant, Employee, Menu, MenuItem
from decorator.has_permission_decorator import has_permission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.serializers_v1 import (
    RestaurantSerializer,
    EmployeeSerializer,
    MenuSerializer,
    MenuItemSerializer,
)
from external.pagination import CustomPagination
from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.user.models import User
from apps.user.serializers.serializers_v1 import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import transaction


@extend_schema(tags=["Restaurant"])
class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializer_class

    @has_permission("create_restaurant")
    def create(self, request, *args, **kwargs):
        if str(request.user.id) != request.data["owner"]:
            return Response(
                {"message": "You can not create restaurant for someone else"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Restaurant created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("update_restaurant")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(request.user.id) != request.data["owner"]:
            return Response(
                {"message": "Ownership changing is not currenty available"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Restaurant updated"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("list_restaurant")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.role == "owner":
            queryset = queryset.filter(owner=request.user.id)
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @has_permission("retrieve_restaurant")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @has_permission("delete_restaurant")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Restaurant deleted"}, status=status.HTTP_204_NO_CONTENT
        )


@extend_schema(tags=["Employee Signup"])
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @transaction.atomic
    @has_permission("create_employee")
    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Employee Example",
                value={
                    "password": "string",
                    "first_name": "string",
                    "last_name": "string",
                    "email": "mail@gmail.com",
                    "username": "string",
                    "profile_pic": "file",
                    "phone_number": "integer",
                    "birth_date": "2024-08-23",
                    "role": "employee",
                    "two_factor": False,
                    "restaurant": "UUID",
                    "salary": "integer",
                },
                request_only=True,
                response_only=False,
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        if request.user.role != "owner":
            return Response(
                {"message": "Employee creation is prohibited without being an owner"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.data["role"] != "employee":
            return Response(
                {"message": "Restricted action. Only employee creation is accepted"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if User.objects.filter(email=request.data["email"]).first():
            return Response(
                {"message": "This email is taken by another user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=request.data["username"]).first():
            return Response(
                {"message": "Username is already in use."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "password" in request.data.keys():
            try:
                validate_password(request.data["password"])
                request.data["password"] = make_password(request.data["password"])
            except ValidationError:
                return Response(
                    {"message": "Given password is too weak."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if "profile_pic" in request.data.keys():
            if request.data["profile_pic"] in ["", None, "null"]:
                request.data.pop("profile_pic")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            employee_data = {
                "user": user.id,
                "restaurant": request.data["restaurant"],
                "salary": request.data.get("salary", 0),
            }
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid(raise_exception=True):
                employee_serializer.save()
            else:
                return Response(
                    {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"message": "Employee Registration success."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @transaction.atomic
    @has_permission("update_employee")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role not in ["owner", "employee"]:
            return Response(
                {"message": "Restricted action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.data["role"] != "employee":
            return Response(
                {"message": "Restricted action. Only employee creation is accepted"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if self.queryset.filter(
            ~Q(id=instance.id), email=request.data["email"]
        ).first():
            return Response(
                {"message": "This email is taken by another user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if self.queryset.filter(
            ~Q(id=instance.id), username=request.data["username"]
        ).first():
            return Response(
                {"message": "Username is already in use."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "password" in request.data.keys():
            try:
                validate_password(request.data["password"])
                request.data["password"] = make_password(request.data["password"])
            except ValidationError:
                return Response(
                    {"message": "Given password is too weak."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if "profile_pic" in request.data.keys():
            if request.data["profile_pic"] in ["", None, "null"]:
                request.data.pop("profile_pic")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            employee_data = {
                "user": user,
                "restaurant": request.data["restaurant"],
                "salary": request.data.get("salary", 0),
            }
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid(raise_exception=True):
                employee_serializer.save()
            else:
                return Response(
                    {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"message": "Employee Registration success."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("list_employee")
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(restaurant__owner=request.user.id)
        if request.user.role != "owner":
            queryset = []
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @has_permission("retrieve_employee")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @has_permission("delete_employee")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Restaurant deleted"}, status=status.HTTP_204_NO_CONTENT
        )


@extend_schema(tags=["Menu"])
class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @has_permission("create_menu")
    def create(self, request, *args, **kwargs):
        restaurant_ids = str(
            request.user.restaurant_owner.all().values_list("id", flat=True)
        )
        if request.data["restaurant"] not in restaurant_ids:
            return Response(
                {"Restricted action. You don't own the restaurant"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Menu created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("update_menu")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        restaurant_ids = str(
            request.user.restaurant_owner.all().values_list("id", flat=True)
        )
        if request.data["restaurant"] not in restaurant_ids:
            return Response(
                {"Restricted action. You don't own the restaurant"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Menu updated"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("list_menu")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        resturant = request.query_params.get("restaurant", None)
        if resturant:
            queryset = queryset.filter(resturant=resturant)
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @has_permission("retrieve_menu")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @has_permission("delete_menu")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Menu deleted"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Menu Item"])
class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    @has_permission("create_menu_item")
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Menu item created"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("list_menu_item")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        menu = request.query_params.get("menu", None)
        if menu:
            queryset = queryset.filter(menu=menu)
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @has_permission("retrieve_menu_item")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @has_permission("update_menu_item")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Menu item updated"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("delete_menuitem")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Menu item deleted"}, status=status.HTTP_204_NO_CONTENT
        )
