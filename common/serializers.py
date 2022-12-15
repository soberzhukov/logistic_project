from rest_framework.serializers import ModelSerializer

from common.models import SavedSearch
from users.serializers import GetUserSerializer


class GetSavedSearchSerializer(ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        model = SavedSearch
        fields = '__all__'
        depth = 1


class CreateDeleteSavedSearchSerializer(ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs
