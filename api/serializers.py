from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CustomUSer, AgentUser, HouseModel
from django.contrib.auth import get_user_model
from cities_light.models import Country, Region

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


class HouseSerializer(ModelSerializer):
    class Meta :
        model = HouseModel
        fields = ["id", "house_name", "house_description", "house_location", 
                  "house_images", "house_price", "house_size", "house_rooms_no", "house_toilet_no",
                   "house_amenties", "house_category", "country", "state", "created_at", "updated_at",
                    ]
    def validate(self, attrs):

        country = attrs.get('country')
        state = attrs.get('state')

        if state and state.country != country:
            raise serializers.ValidationError(
                "State does not belong to selected country."
            )
        
        return attrs
    
    def get_country_name(self, obj):
        return obj.country.name if obj.country else None

    def get_state_name(self, obj):
        return obj.state.name if obj.state else None
    
class AgentProfileSerializer(ModelSerializer):
    class Meta:
        model = AgentUser
        fields = ["first_name","last_name", "about", "phone", "profile_img", ]

class AgentKYCSerializer(ModelSerializer):
    class Meta:
        model = AgentUser
        fields = ["bvn_number", "nin_document" ]

