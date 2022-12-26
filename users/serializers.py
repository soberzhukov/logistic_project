from cities_light.models import Country
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.models import Image
from users.models import ConfirmPhone, User, ConfirmPassword, PassportFiles


class CreateConfirmPhoneSerializer(serializers.ModelSerializer):
    """Сериализатор создания модели подтверждения пользователя"""
    is_authorized = serializers.SerializerMethodField('get_is_authorized')

    class Meta:
        model = ConfirmPhone
        fields = ['phone', 'is_authorized']

    def get_is_authorized(self, obj):
        phone = self._validate_phone(obj.get('phone'))
        if User.objects.filter(username=phone).exists():
            return True
        return False

    def _validate_phone(self, phone: str) -> str:
        if phone != '' and phone is not None:
            phone = PhoneNumber.from_string(phone_number=phone, region='RU').as_e164
            return phone
        else:
            raise ValueError('Phone number is valid')


class ConfirmPhoneSerializer(serializers.ModelSerializer):
    """Сериализатор подтверждения пользователя"""

    class Meta:
        model = ConfirmPhone
        fields = ['phone', 'code']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор авторизации по токену"""

    def validate_username(self, phone):
        try:
            normalized_phone = PhoneNumber.from_string(phone_number=phone, region='RU').as_e164
        except Exception as exc:
            raise serializers.ValidationError({'username': str(exc)})
        return normalized_phone


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя"""

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        copy_data = data.copy()
        phone = copy_data['username']
        try:
            normalized_phone = PhoneNumber.from_string(phone_number=phone, region='RU').as_e164
        except Exception as exc:
            raise serializers.ValidationError({'username': str(exc)})
        if User.objects.filter(username__exact=normalized_phone).exists():
            raise serializers.ValidationError({'username': 'User already exist'})
        copy_data['username'] = normalized_phone
        return super().validate(copy_data)

    @property
    def data(self):
        data = {}
        refresh = CustomTokenObtainPairSerializer.get_token(self.instance)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class CreateConfirmPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор создания модели подтверждения пароля"""

    class Meta:
        model = ConfirmPassword
        fields = ['phone']


class ConfirmPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор подтверждения кода пароля"""

    class Meta:
        model = ConfirmPassword
        fields = ['phone', 'code']


class ResetPasswordSerializer(serializers.Serializer):
    """
    Сериализатор кода и номера
    """
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'error': "Пароли не совпадают"})
        return attrs


class GetUserSerializer(serializers.ModelSerializer):
    """Сериализатор отображение пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


#
# class CitiesLightSerializer(serializers.ModelSerializer):
#     """Сериализатор городов"""
#     name = serializers.CharField(source='alternate_names')
#
#     class Meta:
#         model = City
#         fields = ['id', 'name']


class CountryLightSerializer(serializers.ModelSerializer):
    """Сериализатор стран"""
    name = serializers.CharField(source='alternate_names')

    class Meta:
        model = Country
        fields = ['id', 'name']


class UserInfoSerializer(serializers.ModelSerializer):
    """Сериализатор получения и изменения данных пользователя"""
    country_pk = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='country', write_only=True
    )
    username = serializers.CharField(read_only=True)
    avatar_pk = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source='avatar', write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 'country', 'country_pk', 'push_off',
                  'avatar', 'avatar_pk']
        depth = 1

    def validate_email(self, obj):
        if User.objects.filter(email=obj).exclude(id=self.context.get('request').user.id).exists():
            raise serializers.ValidationError(f"{obj} - уже существует")
        return obj



class PassportFilesSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(read_only=True)

    class Meta:
        model = PassportFiles
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs