from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from core.models import User

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(
                Q(cpf=username) | Q(pis=username) | Q(email=username)
            )
        except User.DoesNotExist:
            return
        if user.check_password(password):            
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None