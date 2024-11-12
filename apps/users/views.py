from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import BasicUserSerializer, CustomTokenObtainPairSerializer, RegisterUserSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.db import transaction


class UserViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = BasicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == "register_user":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "register_user":
            return RegisterUserSerializer
        return super().get_serializer_class()
    
    @transaction.atomic
    @action(detail=False, methods=["POST"], url_path="register-user")
    # @extend_schema(request=RegisterUserSerializer, responses=BasicUserSerializer)
    def register_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["GET"], url_path="get-all-users")
    def get_all_users(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["GET"], url_path="get-user")
    def get_user(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(detail=True, methods=["PUT"], url_path="update-user")
    def update_user(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"], url_path="delete-user")
    def delete_user(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Authenticates user to generate and get access token
    that can be use to grant users access using simplejwt.
    """

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = CustomTokenObtainPairSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        return Response(response_data, status=status.HTTP_201_CREATED)