from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.authentication.views.views_v1 import LoginViewSet, LogoutViewSet, LogoutFromEveryWhereViewSet

urlpatterns = [
    # --------------------------- JWT Token ------------------------ #
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),

    # --------------------------- Login & Logout ------------------------ #
    path("login/", LoginViewSet.as_view({'post': 'create'}), name='login'),
    path("logout/", LogoutViewSet.as_view({'post': 'create'}), name='logout'),
    path('logout/all/', LogoutFromEveryWhereViewSet.as_view({'post': 'create'}), name='logout_all')
]
