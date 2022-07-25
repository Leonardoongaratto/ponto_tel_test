from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from core.api.viewsets import UserViewSet, UserCreateViewSet, Token

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/create', UserCreateViewSet.as_view(), name='create'),
    path('token', Token.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls)),
]
