import ujson
import grequests as requests
from imdbpie import Imdb
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc

imdb = Imdb()

imdbBlueprint = Blueprint('imdb', url_prefix='imdb')


@imdbBlueprint.route('/title/<imdbid>/', methods=['GET', 'OPTIONS'])
@doc.summary("get movie by imdbid")
@doc.consumes({"imdbid": str}, location="path")
@doc.produces({'data': {'movie': object}})
async def title_by_id(request: Request, imdbid: str):
    title = imdb.get_title_by_id(imdbid)
    return json({'data': {'movie': title}})


@imdbBlueprint.route('/search/', methods=['GET', 'OPTIONS'])
@doc.summary("Search movies in imdb")
@doc.consumes({"q": str}, location="query")
@doc.produces({'data': list})
async def search_movie(request: Request):
    movie_query = request.args['q'][0]
    url = [f"https://v2.sg.media-imdb.com/suggests/{movie_query[0]}/{movie_query}.json"]
    rs = (requests.get(u) for u in url)
    # returns AsyncRequest that is auto awaited
    data = requests.map(rs)[0]
    movies = ujson.loads(data.text.split('(')[1].split(')')[0])
    return json({'data': movies['d']})


@imdbBlueprint.route('/popular/', methods=['GET', 'OPTIONS'])
@doc.summary("Most popular movies")
@doc.produces({'data': {'movies': object}})
async def popular_movies(request: Request):
    return json({'data': {'movies': imdb.popular_movies()}})
