from django.contrib.auth import get_user_model
from rest_framework import generics

from user_api.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self) -> get_user_model():
        return self.request.user
