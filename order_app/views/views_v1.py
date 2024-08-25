import random
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from decorator.has_permission_decorator import has_permission
from rest_framework.response import Response
from rest_framework import status, permissions

from external.pagination import CustomPagination
from ..serializers.serializers_v1 import OrderSerializer
from ..models import Orders
from apps.restaurant.models import MenuItem, Employee, Restaurant

@extend_schema(tags=['Order'])
class OrderViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def generate_unique_tracking_id(self):
        while True:
            tracking_id = str(random.randint(10000, 99999)) 
            if not Orders.objects.filter(traking_id=tracking_id).exists():
                return tracking_id

    def order_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            item_id = serializer.validated_data['item'].id
            menu_item = MenuItem.objects.filter(id=item_id, menu__restaurant=kwargs['restaurant']).first()
            if not menu_item:
                return Response({"message": "Menu item does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            if not menu_item.is_available:
                return Response({"message": "Item is not available"}, status=status.HTTP_400_BAD_REQUEST)
            
            tracking_id = self.generate_unique_tracking_id()
            order = serializer.save(user=self.request.user, traking_id=tracking_id)
            response_data = {
                "message": "Order created successfully",
                "tracking_id": order.traking_id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def trak_order(self, request, *args, **kwargs):
        order = Orders.objects.filter(traking_id=request.data['traking_id']).first()
        if order:
            response_data ={
                "item_name": order.item.name,
                "order_date": order.created_at,
                "quantity": order.quantity,
                "item_price": order.item.price,
                "total_price": order.total_price,
                "order_status": order.order_status,
                "payment_status": order.payment_status,
                "image": order.item.image
            }
            return Response(response_data, status=status.HTTP_103_EARLY_HINTS)
        return Response({"message": "Order not fount"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        restaurant = Restaurant.objects.filter(id=restaurant_id).first()
        is_empoly = Employee.objects.filter(user=request.user, restaurant=restaurant).first()
        if is_empoly:
            exclude_status = ['Delivered', 'Rejected', 'Out_of_Stock', 'Cancelled']
            queryset = self.get_queryset()
            queryset = queryset.filter(restaurant=restaurant).exclude(order_status_in=exclude_status)
            page = self.paginate_queryset(queryset)
            serializer_class = self.get_serializer_class()
            if page is not None:
                serializer = serializer_class(page, many=True, context={"request": request})
                return self.get_paginated_response(serializer.data)

            serializer = serializer_class(queryset, many=True, context={"request": request})
            return Response(serializer.data)
        return Response({"message": "You do not have permission to access this order"}, status=status.HTTP_403_FORBIDDEN)


        

    def retrieve_order(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.filter(id=restaurant_id).first()
        is_empoly = Employee.objects.filter(user=request.user, restaurant=restaurant).first()
        if is_empoly:
            queryset = self.get_queryset()
            queryset = queryset.filter(id=kwargs['order_id'], restaurant=restaurant).first()
            if queryset:
                response_data ={
                    "item_name": queryset.item.name,
                    "order_date": queryset.created_at,
                    "quantity": queryset.quantity,
                    "item_price": queryset.item.price,
                    "total_price": queryset.total_price,
                    "order_status": queryset.order_status,
                    "payment_status": queryset.payment_status,
                    "image": queryset.item.image
                }
                return Response(response_data, status=status.HTTP_103_EARLY_HINTS)
            return Response({"message": "Order not fount"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You do not have permission to access this order"}, status=status.HTTP_403_FORBIDDEN)

    
    # def update(self, request, *args, **kwargs):
    #     
        
    
        
    