from rest_framework import viewsets
from .serializers import User_RegistrationSerializer
from accounts.models import User
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = User_RegistrationSerializer
    queryset = User.objects.all()
    