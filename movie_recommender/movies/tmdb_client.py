import os
import requests
from typing import Any, Dict, Optional

class TMDBClient:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = 'https://api.themoviedb.org/3'

    def search_movies(self, query: str, year: Optional[str] = None, genre: Optional[str] = None, page: int = 1, page_size: int = 20) -> Dict:
        params = {
            'query': query,
            'api_key': self.api_key,
            'page': page,
            'page_size': page_size
        }
        if year:
            params['year'] = year
        if genre:
            params['with_genres'] = genre

        response = requests.get(f'{self.base_url}/search/movie', params=params)
        response.raise_for_status()
        return response.json()

    def get_trending(self) -> Dict:
        params = {
            'api_key': self.api_key,
            'time_window': 'week'  # You can change this to 'day' if you want daily trending movies
        }
        response = requests.get(f'{self.base_url}/trending/movie/week', params=params)
        response.raise_for_status()
        return response.json()

    def get_movie_details(self, movie_id: int) -> Dict:
        params = {
            'api_key': self.api_key,
        }
        response = requests.get(f'{self.base_url}/movie/{movie_id}', params=params)
        response.raise_for_status()
        return response.json()

    def get_recommendations(self, movie_id: int) -> Dict:
        params = {
            'api_key': self.api_key,
        }
        response = requests.get(f'{self.base_url}/movie/{movie_id}/recommendations', params=params)
        response.raise_for_status()
        return response.json()