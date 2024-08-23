from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from decorator.has_permission_decorator import has_permission
from external.swagger_query_params import set_query_params
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from external.pagination import CustomPagination
from apps.user.models import User
from apps.user.serializers.serializers_v1 import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserRetrieveSerializer,
)


@extend_schema(tags=["Owner/User Signup"])
class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    model_class = User
    pagination_class = CustomPagination
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        return self.model_class.objects.filter(is_active=True).exclude(
            role="super_user"
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        elif self.request.method == "PUT":
            return UserUpdateSerializer
        elif self.request.method == "GET":
            if "id" in self.kwargs:
                return UserRetrieveSerializer
            else:
                return UserListSerializer
        else:
            return UserCreateSerializer

    # @has_permission("create_user")
    def post(self, request, *args, **kwargs):
        if request.data["role"] == "employee":
            return Response(
                {
                    "message": "Employee registration is not acceptable. Contact your owner"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        if self.model_class.objects.filter(email=request.data["email"]).first():
            return Response(
                {"message": "This email is taken by another user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if self.model_class.objects.filter(username=request.data["username"]).first():
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
            serializer.save()
            return Response(
                {"message": "Registration success."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    # @has_permission("update_user")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"message": "No user found."}, status=status.HTTP_404_NOT_FOUND
            )

        if instance.id != request.user.id:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if self.model_class.objects.filter(
            ~Q(id=instance.id), email=request.data["email"]
        ).first():
            return Response(
                {"message": "This email is taken by another user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if self.model_class.objects.filter(
            ~Q(id=instance.id), username=request.data["username"]
        ).first():
            return Response(
                {"message": "Username is already in use."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "password" in request.data.keys():
            return Response(
                {"message": "Invalid request. Password change restricted."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        if "profile_pic" in request.data.keys():
            if request.data["profile_pic"] in ["", None, "null"]:
                request.data.pop("profile_pic")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Information updated."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    # @has_permission("view_user")
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        # page = self.paginate_queryset(queryset)
        # serializer_class = self.get_serializer_class()
        # if page is not None:
        #     serializer = serializer_class(page, many=True, context={"request": request})
        #     return self.get_paginated_response(serializer.data)

        # serializer = serializer_class(queryset, many=True, context={"request": request})
        # return Response(serializer.data)
        return Response({"message": "Api depricated"}, status=status.HTTP_403_FORBIDDEN)

    # @has_permission("retrieve_user")
    def retrieve(self, request, *args, **kwargs):
        obj = self.model_class.objects.filter(id=kwargs["uuid"]).first()
        if not obj:
            return Response(
                {"message": "No user found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj, many=False, context={"request": request})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # @has_permission("delete_user")
    def destroy(self, request, *args, **kwargs):
        obj = self.model_class.objects.filter(id=kwargs["id"]).first()
        if not obj:
            return Response(
                {"message": "No user found."}, status=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return Response({"message": "Deleted."}, status=status.HTTP_202_ACCEPTED)
