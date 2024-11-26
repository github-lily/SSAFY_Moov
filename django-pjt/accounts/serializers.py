# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Movie
# from .models import Comment
from movies.serializers import MovieSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    profile_img = serializers.CharField(required = False, allow_blank=True, max_length=255)
    level = serializers.CharField(required = False, allow_blank=True, max_length=255)

    # 찜한 영화 
    # like_movies = MovieSerializer(source='user_like_movies', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class CustomUserDetailSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = '__all__'



# 프로필 이미지

class UserImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_img', 'id')

