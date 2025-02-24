from django.db import models
from django.contrib.auth.models import User


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField(default='1970-01-01')
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('user', 'movie_id')
