from rest_framework.serializers import ModelSerializer
from .models import CustomUSer, AgentUser
from django.contrib.auth import get_user_model

class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUSer
        fields = ["username", "email", "password", "roles",]
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        roles = validated_data.pop('roles')
        user = get_user_model()

        validated_user = user.objects.create_user(**validated_data, roles=roles)

        if roles == "Agent":
            AgentUser.objects.create(user=validated_user)

        return validated_user



