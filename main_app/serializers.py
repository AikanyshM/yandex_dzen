from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


    def create(self, validated_data):
        user = User(username=validated_data['username'])
        is_staff=validated_data['is_staff']
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password cannot be less than 8 sumbols")
        return password



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', ]



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', ]