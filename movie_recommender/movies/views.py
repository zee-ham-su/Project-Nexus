from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tmdb_client import TMDBClient
import logging
from django.http import JsonResponse, HttpRequest
import os
from typing import Any, Dict, Optional
from upstash_redis import Redis
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger(__name__)

UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

# Initialize Redis client
redis = Redis(url=UPSTASH_REDIS_REST_URL, token=UPSTASH_REDIS_REST_TOKEN)

def health_check(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "message": "Welcome to the Movie Recommender API!"})

def redis_set(key: str, value: str, ttl: int = 3600) -> Dict[str, Any]:
    """Store data in Upstash Redis."""
    response = redis.set(key, value, ex=ttl)
    print(f"SET {key}: {response}")
    return response

def redis_get(key: str) -> Optional[str]:
    """Retrieve data from Upstash Redis."""
    response = redis.get(key)
    print(f"GET {key}: {response}")
    return response

class TrendingMoviesView(APIView):
    @swagger_auto_schema(tags=["Movies"])
    def get(self, request: HttpRequest) -> Response:
        try:
            cached = redis_get('trending_movies')
            if cached:
                logger.info("Returning cached trending movies")
                return Response(eval(cached))  # Convert string back to object

            client = TMDBClient()
            movies = client.get_trending()
            redis_set('trending_movies', str(movies))  # Store as string
            logger.info("Fetched and cached trending movies")
            return Response(movies)
        except Exception as e:
            logger.error(f"Error fetching trending movies: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class RecommendationsView(APIView):
    @swagger_auto_schema(tags=["Movies"])
    def get(self, request: HttpRequest, movie_id: int) -> Response:
        try:
            cache_key = f'recommendations_{movie_id}'
            cached = redis_get(cache_key)
            if cached:
                logger.info(f"Returning cached recommendations for movie {movie_id}")
                return Response(eval(cached))  # Convert string back to Python object

            client = TMDBClient()
            recommendations = client.get_recommendations(movie_id)
            redis_set(cache_key, str(recommendations))  # Store as string
            logger.info(f"Fetched and cached recommendations for movie {movie_id}")
            return Response(recommendations)
        except Exception as e:
            logger.error(f"Error fetching recommendations for movie {movie_id}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class MovieDetailView(APIView):
    @swagger_auto_schema(tags=["Movies"])
    def get(self, request: HttpRequest, movie_id: int) -> Response:
        try:
            cache_key = f'movie_{movie_id}'
            cached = redis_get(cache_key)
            if cached:
                logger.info(f"Returning cached details for movie {movie_id}")
                return Response(eval(cached))  # Convert string back to Python object

            client = TMDBClient()
            movie_details = client.get_movie_details(movie_id)
            redis_set(cache_key, str(movie_details))  # Store as string
            logger.info(f"Fetched and cached details for movie {movie_id}")
            return Response(movie_details)
        except Exception as e:
            logger.error(f"Error fetching details for movie {movie_id}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class SearchMoviesView(APIView):
    @swagger_auto_schema(
        tags=["Movies"],
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('year', openapi.IN_QUERY, description="Filter by year", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('genre', openapi.IN_QUERY, description="Filter by genre", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of results per page", type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={200: 'Search results'}
    )
    def get(self, request: HttpRequest) -> Response:
        query = request.query_params.get('query')
        year = request.query_params.get('year')
        genre = request.query_params.get('genre')
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)

        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cache_key = f'search_{query}_{year}_{genre}_{page}_{page_size}'
            cached = redis_get(cache_key)
            if cached:
                logger.info(f"Returning cached search results for query: {query}, year: {year}, genre: {genre}, page: {page}, page_size: {page_size}")
                return Response(eval(cached))  # Convert string back to Python object

            client = TMDBClient()
            search_results = client.search_movies(query, year=year, genre=genre, page=page, page_size=page_size)
            redis_set(cache_key, str(search_results))  # Store as string
            logger.info(f"Fetched and cached search results for query: {query}, year: {year}, genre: {genre}, page: {page}, page_size: {page_size}")
            return Response(search_results)
        except Exception as e:
            logger.error(f"Error fetching search results for query {query}, year {year}, genre {genre}, page {page}, page_size {page_size}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)