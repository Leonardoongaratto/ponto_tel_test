from core.models import Address, User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    cpf = serializers.CharField(max_length=11, validators=[UniqueValidator(queryset=User.objects.all())])
    pis = serializers.CharField(max_length=11, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id', 'url', 'cpf', 'email', 'pis', 'address', 'password']
    

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        address_data = validated_data.pop('address') if validated_data.get('address') else None
        user = User.objects.create(**validated_data)
        user.is_active = True

        if address_data:
            address = Address.objects.create(**address_data)
            user.address = address

        user.save()
        return user


    def update(self, instance, validated_data):
        address_data = validated_data.pop('address') if validated_data.get('address') else None
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.pis = validated_data.get('pis', instance.pis)
        if validated_data.get('password'):
            instance.password = make_password(validated_data.get('password'))

        if instance.address:
            instance.address.pais = address_data.get('pais', instance.address.pais)
            instance.address.estado = address_data.get('estado', instance.address.estado)
            instance.address.cidade = address_data.get('cidade', instance.address.cidade)
            instance.address.cep = address_data.get('cep', instance.address.cep)
            instance.address.rua = address_data.get('rua', instance.address.rua)
            instance.address.numero = address_data.get('numero', instance.address.numero)
            instance.address.complemento = address_data.get('complemento', instance.address.complemento)

            instance.address.save()
        elif address_data:
            address = Address.objects.create(**address_data)
            instance.address = address

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class GetTokenSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        del self.fields[self.username_field]
        self.fields["username"] = serializers.CharField()

    def validate(self, attrs):
        serializer = LoginSerializer(data={
            "username": attrs['username'],
            "password": attrs['password']
            }
        )
        serializer.is_valid(raise_exception=True)

        authenticate_kwargs = {
            "username": attrs["username"],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)
        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
