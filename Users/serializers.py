from rest_framework import serializers
from . import models
from django.contrib.auth.password_validation import validate_password
from .models import TeamUser, SoloUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    phone = serializers.CharField(allow_null=True, required=False)
    class Meta:
        model = models.CustomUser
        fields = ['email', 'username', 'phone', 'user_type', 'password', 'password2']
        extra_kwargs = {
         'password':{'write_only':True},
         'password2':{'write_only':True},
         'email':{'required':True},
         'username':{'required':True},
         'phone':{'required':True},
         'user_type':{'required':True},
        }

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user_type = validated_data['user_type']
        if user_type == 'Team':
            user = models.TeamUser.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                phone=validated_data.get('phone'),
                user_type=user_type
            )
        elif user_type == 'Solo':
            user = models.SoloUser.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                phone=validated_data.get('phone'),
                user_type=user_type
            )
        else:
            raise serializers.ValidationError({"user_type": "Invalid user type."})

        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
