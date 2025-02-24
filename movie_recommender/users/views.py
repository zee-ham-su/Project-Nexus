from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import FavoriteMovie
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    FavoriteMovieSerializer
)
from movies.tmdb_client import TMDBClient
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegistrationView(APIView):

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: "User registered successfully", 400: "Invalid data"}
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        request_body=CustomTokenObtainPairSerializer,
        responses={
            200: CustomTokenObtainPairSerializer,
            401: 'Invalid credentials'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class FavoriteMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: FavoriteMovieSerializer(many=True)}
    )
    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)
        serializer = FavoriteMovieSerializer(favorites, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'movie_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the movie')
            }
        ),
        responses={
            201: FavoriteMovieSerializer,
            400: "Invalid movie ID or Movie already in favorites"
        }
    )
    def post(self, request):
        movie_id = request.data.get('movie_id')

        try:
            client = TMDBClient()
            client.get_movie_details(movie_id)
        except Exception as e:
            return Response(
                {"error": f"Invalid movie ID: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if FavoriteMovie.objects.filter(user=request.user, movie_id=movie_id).exists():
            return Response(
                {"error": "Movie already in favorites"},
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite = FavoriteMovie.objects.create(
            user=request.user, movie_id=movie_id)
        serializer = FavoriteMovieSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
