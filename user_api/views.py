from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user_api.schemas.users import user_register_schema
from user_api.serializers import UserSerializer


@user_register_schema
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> get_user_model():
        return self.request.user
