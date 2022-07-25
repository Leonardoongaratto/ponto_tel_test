from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Address(models.Model):
    pais = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    cidade = models.CharField(max_length=20)
    cep = models.CharField(max_length=50)
    rua = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    complemento = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.rua


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Usuário precisa ter um e-mail')
        
        user = self.model(
            email=self.normalize_email(email),
        )

        if password:
            user.set_password(password)
            
        user.is_active = True
        user.save()

        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    pis = models.CharField(max_length=15, unique=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.PROTECT)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    is_active = models.BooleanField(
        verbose_name='Usuário Ativo',
        default=False)
    
    is_staff = models.BooleanField(
        verbose_name='Usuário da Equipe',
        default=False)
    
    is_superuser = models.BooleanField(
        verbose_name='Super Usuário',
        default=False)


    def __str__(self):
        return self.email


