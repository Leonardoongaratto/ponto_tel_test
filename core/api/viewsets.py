from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import User
from .serializers import GetTokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)


class UserCreateViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Token(TokenObtainPairView):
    def get_serializer_class(self):
        return GetTokenSerializer