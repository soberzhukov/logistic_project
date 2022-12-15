from rest_framework.serializers import ModelSerializer

from common.models import SavedSearch
from users.serializers import GetUserSerializer


class GetObjectSerializer(ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        fields = '__all__'
        depth = 1


class UpdateObjectSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs


class GetSavedSearchSerializer(GetObjectSerializer):
    class Meta(GetObjectSerializer.Meta):
        model = SavedSearch


class CreateDeleteSavedSearchSerializer(UpdateObjectSerializer):
    class Meta(UpdateObjectSerializer.Meta):
        model = SavedSearch
