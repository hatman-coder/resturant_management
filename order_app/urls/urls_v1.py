from django.urls import path

from order_app.views.views_v1 import OrderViewSet


urlpatterns = [
    path('order_create/', OrderViewSet.as_view({'post': 'order_create'})),
    path('order-status-update/<str:id>/', OrderViewSet.as_view({'put': 'order_status_update'})),
    path('list/', OrderViewSet.as_view({'get': 'list'})),
    path('retrieve-order/<str:id>/', OrderViewSet.as_view({'get': 'retrieve_order'})),
    path('track-order/<str:traking_id>/', OrderViewSet.as_view({'delete': 'trak_order'}))
]
