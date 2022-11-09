from drf_yasg import openapi
from rest_framework import serializers


class TokenSchemaSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class LoginSchema:
    response: dict = {
        "200": openapi.Response(
            description="Успешный вывод",
            schema=TokenSchemaSerializer,
            examples={
                "application/json": {
                    "access": "asdsadsad",
                    "refresh": "hkjhakjhdjkhkj",
                }
            }
        )
    }


class ErrorResponseSchema(serializers.Serializer):
    message = serializers.CharField()
    code = serializers.CharField()


class TokenResponseSchema(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class RegistrationSchema:
    response: dict = {
        "200": openapi.Response(
            description="Успешный вывод",
            schema=TokenResponseSchema,
            examples={
                "application/json": {
                    "access": "sadsadasdasdsadasd",
                    "refresh": "sadsadasdasdasdasd",
                }
            }
        ),
        "403": openapi.Response(
            description="Не подтвержден номер телефона",
            schema=ErrorResponseSchema,
            examples={
                "application/json": {
                    "message": "Phone not verified",
                    "code": "not_verified",
                }
            }
        ),
        "400": openapi.Response(
            description="Такой пользователь уже существует",
            schema=ErrorResponseSchema,
            examples={
                "application/json": {
                    "username": ["User already exist"],
                }
            }
        )
    }
