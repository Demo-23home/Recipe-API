from rest_framework import generics
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a user in the system.
    """
    serializer_class = UserSerializer