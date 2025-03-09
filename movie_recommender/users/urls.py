from django.urls import path
from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    FavoriteMoviesView,
    FavoriteMovieDetailView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CustomTokenObtainPairView.as_view(), name='token-refresh'),
    path('favorites/', FavoriteMoviesView.as_view(), name='auth-favorites-list-create'),
    path('favorites/<int:id>/', FavoriteMovieDetailView.as_view(), name='auth-favorites-delete'),
]