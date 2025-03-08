from django.urls import path
from .views import TrendingMoviesView, RecommendationsView, health_check

urlpatterns = [
    path('movies/trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('movies/<int:movie_id>/recommendations/',
         RecommendationsView.as_view(), name='movie-recommendations'),
    path('health-check/', health_check, name='health-check'),
]
