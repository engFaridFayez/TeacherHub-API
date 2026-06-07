from rest_framework import serializers

from core.serializers import StageSerializer
from users.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "username",
            "password",
            "confirm_password",
            "phone",
            "address",
            "whatsapp",
            "birth_date",
            "parent_phone",
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self,attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
            "Password and Confirm Password do not match."
        )
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('confirm_password')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            full_name = validated_data['full_name'],
            phone = validated_data['phone'],
            address = validated_data['address'],
            whatsapp = validated_data['whatsapp'],
            birth_date = validated_data['birth_date'],
            parent_phone = validated_data['parent_phone'],
        )

        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    stage = StageSerializer()
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'full_name',
            'first_name',
            'last_name',
            'birth_date',
            'email',
            'image',
            'address',
            'phone',
            'role',
            'stage',
            'slogan',
            'parent_phone',
            'whatsapp',

        ]