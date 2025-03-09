from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from movies.views import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="Movie Recommendation API",
        default_version='v1',
        description="API for movie recommendations and user preferences",
    ),
    public=True,
)

urlpatterns = [
    path("", health_check, name="home"),
    path('admin/', admin.site.urls),
    path('api/v1/', include('movies.urls')),
    path('api/v1/auth/', include('users.urls')),
    path('api/docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
