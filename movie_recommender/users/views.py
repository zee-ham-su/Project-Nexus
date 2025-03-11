from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
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
        tags=["Authentication"],
        request_body=UserRegistrationSerializer,
        responses={201: "User registered successfully", 400: "Invalid data"}
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        tags=["Authentication"],
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
        tags=["Favorite Movies"],
        responses={200: FavoriteMovieSerializer(many=True)}
    )
    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)
        serializer = FavoriteMovieSerializer(favorites, many=True)
        return Response(
            {
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email
                },
                "favorite_movies": serializer.data
            }
        )

    @swagger_auto_schema(
        tags=["Favorite Movies"],
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
            movie_details = client.get_movie_details(movie_id)
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
            user=request.user,
            movie_id=movie_id,
            title=movie_details.get('title'),
            overview=movie_details.get('overview'),
            release_date=movie_details.get('release_date'),
            backdrop_path=movie_details.get('backdrop_path'),
            poster_path=movie_details.get('poster_path')
        )
        serializer = FavoriteMovieSerializer(favorite)
        return Response(
            {
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email
                },
                "favorite_movie": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class FavoriteMovieDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Favorite Movies"],
        responses={
            204: "Movie removed from favorites",
            404: "Favorite movie not found"
        }
    )
    def delete(self, request, id):
        try:
            favorite = FavoriteMovie.objects.get(
                user=request.user, movie_id=id)
            favorite.delete()
            return Response(
                {
                    "message": "Movie removed from favorites",
                    "user": {
                        "id": request.user.id,
                        "username": request.user.username,
                        "email": request.user.email
                    }
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except FavoriteMovie.DoesNotExist:
            return Response(
                {"error": "Favorite movie not found"},
                status=status.HTTP_404_NOT_FOUND
            )
