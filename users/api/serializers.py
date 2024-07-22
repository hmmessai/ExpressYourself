from rest_framework import serializers
from users.models import CustomUser, CustomerProfile, SellerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

