from .models import FavoriteMovie
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from movies.tmdb_client import TMDBClient


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'favourite_count': FavoriteMovie.objects.filter(user=self.user).count()
        }
        return data


class FavoriteMovieSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    poster_path = serializers.SerializerMethodField()
    overview = serializers.SerializerMethodField()
    release_date = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteMovie
        fields = ('movie_id', 'created_at', 'title',
                  'overview', 'release_date', 'poster_path')
        read_only_fields = ('created_at',)

    def get_title(self, obj):
        client = TMDBClient()
        details = client.get_movie_details(obj.movie_id)
        return details.get('title')

    def get_poster_path(self, obj):
        client = TMDBClient()
        details = client.get_movie_details(obj.movie_id)
        return details.get('poster_path')

    def get_overview(self, obj):
        client = TMDBClient()
        details = client.get_movie_details(obj.movie_id)
        return details.get('overview')

    def get_release_date(self, obj):
        client = TMDBClient()
        details = client.get_movie_details(obj.movie_id)
        return details.get('release_date')
