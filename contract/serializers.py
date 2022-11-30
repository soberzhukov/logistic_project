# from rest_framework.serializers import ModelSerializer

# from payment.models import Contract
# from users.serializers import GetUserSerializer
#
#
# class GetContractSerializer(ModelSerializer):
#     author = GetUserSerializer()
#
#     class Meta:
#         model = Contract
#         fields = '__all__'
#
#
# class UpdateContractSerializer(ModelSerializer):
#     class Meta:
#         model = Contract
#         fields = '__all__'
#
#     def validate(self, attrs):
#         attrs['author'] = self.context['request'].user
#         return attrs
