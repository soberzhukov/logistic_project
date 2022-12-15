from rest_framework import serializers

from common.models import SavedSearch
from payment.models import Budget
from payment.serializers import BudgetSerializer
from users.serializers import GetUserSerializer


class GetObjectSerializer(serializers.ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        fields = '__all__'
        depth = 1


class UpdateObjectSerializer(serializers.ModelSerializer):
    budget = BudgetSerializer()

    class Meta:
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        budget_data = validated_data.pop('budget')
        budget = Budget(**budget_data)
        budget.save()
        validated_data['budget'] = budget
        instance = super().create(validated_data)
        return instance


class GetSavedSearchSerializer(GetObjectSerializer):
    class Meta(GetObjectSerializer.Meta):
        model = SavedSearch


class CreateDeleteSavedSearchSerializer(UpdateObjectSerializer):
    class Meta(UpdateObjectSerializer.Meta):
        model = SavedSearch
