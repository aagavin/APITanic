import os
import ujson
import requests
import lxml
from lxml import html
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc

imdbBlueprint = Blueprint('imdb', url_prefix='imdb')


@imdbBlueprint.route('/title/<imdbid>/', methods=['GET', 'OPTIONS'])
@doc.summary("get movie by imdbid")
@doc.consumes({"imdbid": str}, location="path")
@doc.produces({'data': {'movie': object}})
async def title_by_id(request: Request, imdbid: str):
    api_key = os.getenv('openapikey')
    url = f'https://www.omdbapi.com/?i={imdbid}&apikey={api_key}'
    data = requests.get(url)
    return json({'data': {'movie': data.json()}})


@imdbBlueprint.route('/search/', methods=['GET', 'OPTIONS'])
@doc.summary("Search movies in imdb")
@doc.consumes({"q": str}, location="query")
@doc.produces({'data': list})
async def search_movie(request: Request):
    movie_query = request.args['q'][0]
    url = f'https://v2.sg.media-imdb.com/suggests/{movie_query[0]}/{movie_query}.json'
    rs = requests.get(url)
    data = rs.text
    movies = ujson.loads(data.split('(')[1].split(')')[0])
    return json({'data': movies['d']})


@imdbBlueprint.route('/popular/', methods=['GET', 'OPTIONS'])
@doc.summary("Most popular movies")
@doc.produces({'data': {'movies': object}})
async def popular_movies(request: Request):
    popular_url = 'http://www.imdb.com/chart/moviemeter'
    data = requests.get(popular_url).text
    raw_string = lxml.html.fromstring(data)

    posters = raw_string.xpath('//td[@class=\'posterColumn\']/a')
    titles = raw_string.xpath('//td[@class=\'titleColumn\']/a')
    ratings = raw_string.xpath('//td[@class=\'ratingColumn imdbRating\']')

    popular_movies_list: list = []

    for i in range(50):
        # ratings[i].getchildren()
        movie = {
            'imdbid': posters[i].attrib['href'].split('/')[2],
            'title': titles[i].text,
            'poster_url': posters[i].find('img').attrib['src'],
            'people': titles[i].attrib['title'],
            # 'rating': ratings[i].text
        }
        if ratings[i].find('strong') is not None:
            movie['rating'] = ratings[i].find('strong').text
        else:
            movie['rating'] = None
        popular_movies_list.append(movie)

    return json({'data': {'movies': popular_movies_list}})
