from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import password_validation

class UserSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value
 
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                       username=validated_data['username']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user': self.user.username})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['email', 'mobile_number', 'country','user_photo']
        
