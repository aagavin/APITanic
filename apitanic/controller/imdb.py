import os
import ujson
import requests
import lxml
from lxml import html
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc
from functools import lru_cache
from apitanic.model.imdb import ImdbModel

imdbBlueprint = Blueprint('imdb', url_prefix='imdb')
imdb = ImdbModel()


@lru_cache(maxsize=64)
@imdbBlueprint.route('/title/<imdbid>/', methods=['GET'])
@doc.summary("get movie by imdbid")
@doc.description("Returns a movie object by the imdb id")
@doc.consumes({"imdbid": str}, location="path")
@doc.produces({'data': {'movie': object}})
async def title_by_id(request: Request, imdbid: str):
    return json({'data': {'movie': await imdb.get_by_id(imdbid)}})


@lru_cache(maxsize=64)
@imdbBlueprint.route('/search/', methods=['GET'])
@doc.summary("Search imdb")
@doc.description("Searches imdb for a movie")
@doc.consumes({"q": str}, location="query")
@doc.produces({'data': list})
async def search_movie(request: Request):
    movie_query = request.args['q'][0].replace(' ', '_').lower()
    return json({'data': await imdb.search(movie_query)})


@lru_cache(maxsize=5)
@imdbBlueprint.route('/popular/', methods=['GET'])
@doc.summary('Most popular movies')
@doc.description('Gets the most popular movies at time of request')
@doc.consumes(None)
@doc.produces({'data': {'movies': object}})
async def popular_movies(request: Request):
    return json({'data': {'movies': await imdb.get_popular_movies()}})
