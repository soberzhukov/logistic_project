from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from offer.models import Offer, ElectedOffer
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


class GetElectedOfferSerializer(ModelSerializer):
    user = GetUserSerializer()

    class Meta:
        model = ElectedOffer
        fields = '__all__'
        depth = 1


class UpdateElectedOfferSerializer(ModelSerializer):
    class Meta:
        model = ElectedOffer
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        if ElectedOffer.objects.filter(user=user, offer=attrs.get('offer')).exists():
            raise serializers.ValidationError([f"{attrs['offer'].id} - already exists."])
        return attrs
