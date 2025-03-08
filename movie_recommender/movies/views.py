from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .tmdb_client import TMDBClient
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)





def health_check(request):
    return JsonResponse({"status": "ok", "message": "Welcome to the Movie Recommender API!"})


class TrendingMoviesView(APIView):
    def get(self, request):
        try:
            cached = cache.get('trending_movies')
            if cached:
                logger.info("Returning cached trending movies")
                return Response(cached)

            client = TMDBClient()
            movies = client.get_trending()
            cache.set('trending_movies', movies, timeout=3600)  # 1 hour cache
            logger.info("Fetched and cached trending movies")
            return Response(movies)
        except Exception as e:
            logger.error(f"Error fetching trending movies: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RecommendationsView(APIView):
    def get(self, request, movie_id):
        try:
            cache_key = f'recommendations_{movie_id}'
            cached = cache.get(cache_key)
            if cached:
                logger.info(
                    f"Returning cached recommendations for movie {movie_id}")
                return Response(cached)

            client = TMDBClient()
            recommendations = client.get_recommendations(movie_id)
            cache.set(cache_key, recommendations, timeout=3600)
            return Response(recommendations)
        except Exception as e:
            logger.error(
                f"Error fetching recommendations for movie {movie_id}: {str(e)}")

            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
