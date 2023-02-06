from cities_light.models import Country
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from common.models import File
from common.serializers import FileSerializer
from users.models import ConfirmPhone, User, ConfirmPassword, PassportFiles, ConfirmMail


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


class CodeCustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор авторизации по коду"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields["code"] = serializers.CharField(min_length=6, max_length=6)

    def validate_username(self, phone):
        try:
            normalized_phone = PhoneNumber.from_string(phone_number=phone, region='RU').as_e164
        except Exception as exc:
            raise serializers.ValidationError({'username': str(exc)})
        return normalized_phone

    def validate(self, attrs):
        data = {}

        self.user = User.objects.get(username=attrs['username'])
        self.custom_validate_code(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    def custom_validate_code(self, attrs):
        instance = ConfirmPhone.objects.filter(phone=attrs['username']).last()
        if not instance:
            raise serializers.ValidationError({'code': 'Not found code'})
        if instance.code != attrs['code']:
            raise serializers.ValidationError({'code': 'Wrong code'})
        if instance.expired_time < timezone.now():
            raise serializers.ValidationError({'code': 'Expired time'})
        return instance


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
        queryset=File.objects.all(), source='avatar', write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 'country', 'country_pk', 'push_off',
                  'avatar', 'avatar_pk', 'is_verified']
        depth = 1

    def validate_email(self, obj):
        if User.objects.filter(email=obj).exclude(id=self.context.get('request').user.id).exists():
            raise serializers.ValidationError(f"{obj} - уже существует")
        return obj


class PassportFilesSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(read_only=True)
    main_page_file = FileSerializer(read_only=True, source='main_page')
    registration_page_file = FileSerializer(read_only=True, source='registration_page')
    selfie_with_passport_file = FileSerializer(read_only=True, source='selfie_with_passport')

    class Meta:
        model = PassportFiles
        fields = '__all__'
        extra_kwargs = {'main_page': {'required': True, 'write_only': True},
                        'registration_page': {'required': True, 'write_only': True},
                        'selfie_with_passport': {'required': True, 'write_only': True}}

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs


class CreateConfirmMailSerializer(serializers.ModelSerializer):
    """Сериализатор создания модели подтверждения пароля"""

    class Meta:
        model = ConfirmMail
        fields = ['email']


class ConfirmMailSerializer(serializers.ModelSerializer):
    """Сериализатор подтверждения кода пароля"""

    class Meta:
        model = ConfirmMail
        fields = ['email', 'code']
