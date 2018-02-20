import os
import requests


class MediaModel:

    def __init__(self):
        self.APIKEY = os.getenv('APIKEY')
        self.BASE_URL = 'https://api.themoviedb.org/3/'
        self.db_urls = {
            'now_playing': self.build_url('movie/now_playing'),
            'now_tv': self.build_url('tv/popular'),
            'movie_id': self.build_url('movie/{movie_id}'),
            'tv_id': self.build_url('tv/{tv_id}'),
            'search': self.build_url('search/multi'),

        }

    def build_url(self, path: str) -> str:
        return f'{self.BASE_URL}{path}?api_key={self.APIKEY}'

    async def get_movie_by_id(self, movie_id: str) -> dict:
        return requests.get(self.db_urls['movie_id'].replace('{movie_id}', movie_id)).json()

    async def get_tv_by_id(self, tv_id: str) -> dict:
        return requests.get(self.db_urls['tv_id'].replace('{tv_id}', tv_id)).json()

    async def get_upcoming_movies(self) -> dict:
        return requests.get(self.db_urls['now_playing']).json()['results']

    async def get_popular_tv(self) -> dict:
        return requests.get(self.db_urls['now_tv']).json()['results']

    async def search(self, query) -> list:
        return requests.get(self.db_urls['search']+f'&query={query}&page=1').json()['results']
