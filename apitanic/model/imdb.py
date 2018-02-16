import requests
import ujson
from imdbpie import Imdb


class ImdbModel:

    def __init__(self):
        self.imdb = Imdb()

    async def get_by_id(self, id:str) -> dict:
        return self.imdb.get_title(id)

    async def get_popular_movies(self) -> dict:
        return self.imdb.get_popular_movies()

    async def get_popular_tv(self) -> dict:
        return self.imdb.get_popular_shows()

    async def search(self, movie_query) -> list:
        url = f'https://v2.sg.media-imdb.com/suggests/{movie_query[0]}/{movie_query}.json'
        rs = requests.get(url)
        data = rs.text
        movies = ujson.loads(data.split('${}('.format(movie_query))[1][:-1])
        return [m for m in movies['d'] if m.get('q') is not None and m['q'] == 'feature']