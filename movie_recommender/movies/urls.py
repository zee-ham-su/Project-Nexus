from django.urls import path
from .views import TrendingMoviesView, RecommendationsView

urlpatterns = [
    path('movies/trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('movies/<int:movie_id>/recommendations/',
         RecommendationsView.as_view(), name='movie-recommendations'),
]
