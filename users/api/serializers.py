from rest_framework import serializers
from users.models import CustomUser, CustomerProfile, SellerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_active',
            'date_joined',
            'last_login',
            ]

