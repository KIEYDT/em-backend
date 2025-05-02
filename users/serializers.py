import logging

from django.contrib.auth import authenticate
from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Organizer
from event.models import Event

class UserSerializer(serializers.ModelSerializer) :
    organizer = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Organizer.objects.all(),
        required=False,
        allow_null=True  # optional but good to add
    )

    class Meta :
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name', 'organizer']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer) :
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
    def validate(self, attrs) :
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }
        user = authenticate(**credentials)

        if user :
            return super().validate({
                'username': user.username,
                'password': attrs.get('password'),
            })
        raise serializers.ValidationError('Invalid credentials')
    

class OrganizerSerializer(serializers.ModelSerializer) :
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta :
        model = Organizer
        fields = ['user', 'name', 'bio', 'events', 'attendance', 'date_joined']