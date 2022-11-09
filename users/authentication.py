from django.utils import timezone

from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        user.last_online = timezone.now()
        user.save()
        return user
