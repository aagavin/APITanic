from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc
from functools import lru_cache
from apitanic.model.media import MediaModel

mediaBlueprint = Blueprint('imdb', url_prefix='imdb')
mediaModel = MediaModel()


@lru_cache(maxsize=64)
@mediaBlueprint.route('/movie/<movie_id>/', methods=['GET'])
@doc.summary("get movie by movie_id")
@doc.description("Returns a movie object by movie_id")
@doc.consumes({"movie_id": str}, location="path")
@doc.produces({'data': {'movie': object}})
async def title_by_id(request: Request, movie_id: str):
    return json({'data': {'movie': await mediaModel.get_movie_by_id(movie_id)}})


@lru_cache(maxsize=64)
@mediaBlueprint.route('/tv/<id>/', methods=['GET'])
@doc.summary("get tv by id")
@doc.description("Returns a tv object by id")
@doc.consumes({"id": str}, location="path")
@doc.produces({'data': {'movie': object}})
async def title_by_id(request: Request, id: str):
    return json({'data': {'movie': await mediaModel.get_movie_by_id(id)}})


@lru_cache(maxsize=64)
@mediaBlueprint.route('/search/', methods=['GET'])
@doc.summary("Search imdb")
@doc.description("Searches imdb for a movie")
@doc.consumes({"q": str}, location="query")
@doc.produces({'data': list})
async def search_movie(request: Request):
    movie_query = request.args['q'][0].replace(' ', '_').lower()
    return json({'data': await mediaModel.search(movie_query)})


@lru_cache(maxsize=5)
@mediaBlueprint.route('/popular/movies', methods=['GET'])
@doc.summary('upcoming movies')
@doc.description('Gets the most popular movies at time of request')
@doc.consumes(None)
@doc.produces({'data': {'movies': object}})
async def popular_movies(request: Request):
    return json({'data': {'movies': await mediaModel.get_upcoming_movies()}})


@lru_cache(maxsize=5)
@mediaBlueprint.route('/popular/tv', methods=['GET'])
@doc.summary('upcoming tv')
@doc.description('Gets the most tv shows time of request')
@doc.consumes(None)
@doc.produces({'data': {'movies': object}})
async def popular_movies(request: Request):
    return json({'data': {'movies': await mediaModel.get_popular_tv()}})
