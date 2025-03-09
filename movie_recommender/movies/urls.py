from django.urls import path
from .views import TrendingMoviesView, RecommendationsView, health_check, SearchMoviesView, MovieDetailView

urlpatterns = [
    path('movies/trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('movies/<int:movie_id>/recommendations/', RecommendationsView.as_view(), name='movie-recommendations'),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='movie-details'),
    path('movies/search/', SearchMoviesView.as_view(), name='search-movies'),
    path('health-check/', health_check, name='health-check'),
]