from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tmdb_client import TMDBClient
import logging
from django.http import JsonResponse, HttpRequest, HttpResponse
import os
import requests
from typing import Any, Dict, Optional
from upstash_redis import Redis

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
    def get(self, request: HttpRequest) -> Response:
        try:
            cached = redis_get('trending_movies')
            if cached:
                logger.info("Returning cached trending movies")
                return Response(eval(cached))  # Convert string back to Python object

            client = TMDBClient()
            movies = client.get_trending()
            redis_set('trending_movies', str(movies))  # Store as string
            logger.info("Fetched and cached trending movies")
            return Response(movies)
        except Exception as e:
            logger.error(f"Error fetching trending movies: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class RecommendationsView(APIView):
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