from rest_framework import viewsets
from .serializers import UserSerializer
from ..models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.request.user.id
        return CustomUser.objects.filter(id=id)