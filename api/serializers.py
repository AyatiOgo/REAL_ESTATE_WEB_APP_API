from rest_framework.serializers import ModelSerializer
from .models import CustomUSer, AgentUser
from django.contrib.auth import get_user_model

class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUSer
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = get_user_model()

        validated_user = user.objects.create_user(**validated_user, role=role)

        if role == "Agent":
            AgentUser.objects.create(user=validated_user)

        return validated_user



