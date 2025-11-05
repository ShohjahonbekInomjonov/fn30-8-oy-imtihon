from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Genre, Movie, Comment, Like


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at', 'movie']


class MovieSerializer(serializers.ModelSerializer):
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source='genre',
        required=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'movie', 'movie_title', 'like', 'created_at']