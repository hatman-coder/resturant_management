from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from apps.password_management.serializers.serializers_v1 import *
from apps.user.models import User


@extend_schema(tags=["Password Management"])
class PasswordChangeViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action == "create":
            return PasswordChangeSerializer
        else:
            return PasswordChangeSerializer

    def create(self, request, *args, **kwargs):
        if not isinstance(request.user, AnonymousUser):
            if request.user.check_password(request.data["old_password"]):
                return Response(
                    {"message": "Wrong password."}, status=HTTP_400_BAD_REQUEST
                )
            if request.data["new_password"] != request.data["confirm_password"]:
                return Response(
                    {"message": "Password did not match"},
                    status=HTTP_406_NOT_ACCEPTABLE,
                )
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, many=False)
            if serializer.is_valid():
                if not request.user.is_superuser or request.user.role not in [
                    "super_user"
                ]:
                    try:
                        validate_password(request.data["new_password"])
                    except ValidationError:
                        return Response(
                            {"message": "Given password is too weak."},
                            status=HTTP_400_BAD_REQUEST,
                        )
                request.data["password"] = make_password(request.data["new_password"])
                request.user.set_password(request.data["new_password"])
                request.user.save()
                update_session_auth_hash(request, request.user)
                return Response({"Password changed."}, status=HTTP_202_ACCEPTED)
            else:
                return Response({"message": serializer.errors}, HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "You are not authorized to do this action"},
                status=HTTP_401_UNAUTHORIZED,
            )


@extend_schema(tags=["Password Management"])
class PasswordResetViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "create":
            return []
        return []

    def get_serializer_class(self):
        if self.action == "create":
            return PasswordResetSerializer
        else:
            return PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        instance = User.active_objects.filter(email=request.data["email"]).first()
        if instance:
            pass
        return Response(
            {
                "message": "If the provided email is valid, we will send you a reset link."
            },
            status=HTTP_202_ACCEPTED,
        )
