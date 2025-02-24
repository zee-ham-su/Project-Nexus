import requests
import os


class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')

    def get_trending(self):
        url = f"{self.BASE_URL}/trending/movie/week"
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('results', [])

    def get_recommendations(self, movie_id):
        url = f"{self.BASE_URL}/movie/{movie_id}/recommendations"
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('results', [])
