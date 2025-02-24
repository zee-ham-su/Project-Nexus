from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .tmdb_client import TMDBClient


class TrendingMoviesView(APIView):
    def get(self, request):
        try:
            cached = cache.get('trending_movies')
            if cached:
                return Response(cached)

            client = TMDBClient()
            movies = client.get_trending()
            cache.set('trending_movies', movies, timeout=3600)  # 1 hour cache
            return Response(movies)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RecommendationsView(APIView):
    def get(self, request, movie_id):
        try:
            cache_key = f'recommendations_{movie_id}'
            cached = cache.get(cache_key)
            if cached:
                return Response(cached)

            client = TMDBClient()
            recommendations = client.get_recommendations(movie_id)
            cache.set(cache_key, recommendations, timeout=3600)
            return Response(recommendations)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
