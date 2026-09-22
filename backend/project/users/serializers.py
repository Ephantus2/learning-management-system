from rest_framework import serializers
from django.conf import settings
from .models import User, LecturerProfile, StudentProfile
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['login_id','first_name', 'last_name', 'email', 'password', 'confirm_password']
        
    
    def validate_login_id(self, value):
        if User.objects.filter(login_id=value).exists():
            raise serializers.ValidationError('login id already exists')
        return value
    
    def validate_email(self, value):
        email_regex = r'^[A-Za-z0-9._-]+@[A-Za-z0-9._-]+\.[A-Za-z0-9._-]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError('Enter a valid email address')
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exists')
        return value
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError('passwords do not match')
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError({'password': 'password Must contain capital letter'})
        if not re.search(r'\d', password):
            raise serializers.ValidationError({'password': 'password must contain a number'})
        if not re.search(r'[.-_$,#!@:;?/*&]', password):
            raise serializers.ValidationError({'password': 'password must contain a special character'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        user = User.objects.create_user(
            login_id= validated_data['login_id'],
            email= validated_data['email'],
            password= validated_data['password']
        )
        
        return user

class StudentProfileSerilizer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"
        read_only_fields = ['user']

class LecturerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = "__all__"
        read_only_fields = ['user']