from django.urls import path
from apps.user.views.views_v1 import UserViewSet

urlpatterns = [
    # --------------------------- User Model ------------------------ #
    path('create/', UserViewSet.as_view({'post': 'post'})),
    path('update/<str:id>/', UserViewSet.as_view({'put': 'put'})),
    path('list/', UserViewSet.as_view({'get': 'list'})),
    path('retrieve/<str:id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('delete/<str:id>/', UserViewSet.as_view({'delete': 'destroy'}))
]
