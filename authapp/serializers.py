from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token, if needed
        # token['custom_claim'] = 'custom_value'

        return token



