from django.urls import path
from ..views.views_v1 import PasswordChangeViewSet, PasswordResetViewSet

urlpatterns = [
    path('change/', PasswordChangeViewSet.as_view({'post': 'create'})),
    # path('reset/', PasswordResetViewSet.as_view({'post', 'create'}))
]
