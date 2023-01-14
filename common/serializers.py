from rest_framework import serializers

from common.models import SavedSearch, File
from payment.models import Budget
from payment.serializers import BudgetSerializer
from users.models import User


class CommonGetUserSerializer(serializers.ModelSerializer):
    """Сериализатор отображение пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class GetObjectSerializer(serializers.ModelSerializer):
    author = CommonGetUserSerializer()
    budgets = BudgetSerializer(many=True)

    class Meta:
        fields = '__all__'
        depth = 1


class UpdateObjectSerializer(serializers.ModelSerializer):
    budgets = BudgetSerializer(many=True)

    class Meta:
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        budgets_data = validated_data.pop('budgets')
        instance = super().create(validated_data)
        for budget_data in budgets_data:
            budget = Budget(**budget_data)
            budget.save()
            instance.budgets.add(budget)

        return instance

    def update(self, instance, validated_data):

        if budgets_data := validated_data.get('budgets'):
            budget = BudgetSerializer(many=True, data=budgets_data)
            budget.is_valid(raise_exception=True)

            validated_data.pop('budgets')

        instance = super().update(instance, validated_data)
        if budgets_data:
            for budget_data in budgets_data:
                budget = Budget(**budget_data)
                budget.save()
                instance.budgets.add(budget)

        return instance


class GetSavedSearchSerializer(GetObjectSerializer):
    class Meta(GetObjectSerializer.Meta):
        model = SavedSearch


class CreateDeleteSavedSearchSerializer(UpdateObjectSerializer):
    class Meta(UpdateObjectSerializer.Meta):
        model = SavedSearch


class FileSerializer(serializers.ModelSerializer):
    """Сериазитор  файла"""

    class Meta:
        model = File
        fields = ['id', 'file']


class CreateFileSerializer(serializers.Serializer):
    """Сериазитор сохранения файла"""
    file = serializers.CharField(required=True)
    extensions = serializers.CharField(required=True)
