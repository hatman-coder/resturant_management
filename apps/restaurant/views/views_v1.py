from rest_framework.viewsets import ModelViewSet
from ..models import Restaurant, Menu, MenuItem
from decorator.has_permission_decorator import has_permission
from rest_framework.response import Response
from rest_framework import status
from ..serializers.serializers_v1 import RestaurantSerializer, MenuSerializer


class RestaurantModelViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_class(self):
        return self.serializer_class

    @has_permission("create_restaurant")
    def create(self, request, *args, **kwargs):
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
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @has_permission("create_menu")
    def create(self, request, *args, **kwargs):
        if request.user.restaurant_owner != request.data["restaurant"]:
            return Response(
                {"Restricted action. You dont own the restaurant"},
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

    @has_permission("list_menu")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @has_permission("retrieve_menu")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @has_permission("update_menu")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Menu updated"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    @has_permission("delete_menu")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Menu deleted"}, status=status.HTTP_204_NO_CONTENT)
