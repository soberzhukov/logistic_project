from rest_framework.serializers import ModelSerializer

from offer.models import Offer
from users.serializers import GetUserSerializer


class GetOfferSerializer(ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        model = Offer
        fields = '__all__'
        depth = 1


class UpdateOfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs


