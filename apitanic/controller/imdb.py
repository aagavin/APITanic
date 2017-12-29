import ujson
import grequests as requests
from imdbpie import Imdb
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint

imdb = Imdb()

imdbBlueprint = Blueprint('imdb', url_prefix='imdb')


@imdbBlueprint.route('/title/<imdbid>', methods=['GET'])
async def title_by_id(request: Request, imdbid: str):
    title = imdb.get_title_by_id(imdbid)
    return json(***REMOVED***'data': title***REMOVED***)


@imdbBlueprint.route('/search', methods=['GET'])
async def search_movie(request: Request):
    movie_query = request.args['q'][0]
    url = [f"https://v2.sg.media-imdb.com/suggests/***REMOVED***movie_query[0]***REMOVED***/***REMOVED***movie_query***REMOVED***.json"]
    rs = (requests.get(u) for u in url)
    # returns AsyncRequest that is auto awaited
    data = requests.map(rs)[0]
    movies = ujson.loads(data.text.split('(')[1].split(')')[0])
    return json(***REMOVED***'data': movies['d']***REMOVED***)


@imdbBlueprint.route('/popular', methods=['GET'])
async def popular_movies(request: Request):
    return json(***REMOVED***'data': ***REMOVED***'movies': imdb.popular_movies()***REMOVED******REMOVED***)
