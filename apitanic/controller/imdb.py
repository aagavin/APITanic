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
@doc.description("Returns a movie object by the imdb id")
@doc.consumes({"imdbid": str}, location="path")
@doc.produces({'data': {'movie': object}})
async def title_by_id(request: Request, imdbid: str):
    api_key = os.getenv('openapikey')
    url = 'https://www.omdbapi.com/?i={}&apikey={}'.format(imdbid, api_key)
    data = requests.get(url)
    return json({'data': {'movie': data.json()}})


@imdbBlueprint.route('/search/', methods=['GET', 'OPTIONS'])
@doc.summary("Search imdb")
@doc.description("Searches imdb for a movie")
@doc.consumes({"q": str}, location="query")
@doc.produces({'data': list})
async def search_movie(request: Request):
    movie_query = request.args['q'][0].replace(' ', '_').lower()
    url = 'https://v2.sg.media-imdb.com/suggests/{}/{}.json'.format(movie_query[0], movie_query)
    rs = requests.get(url)
    data = rs.text
    movies = ujson.loads(data.split('${}('.format(movie_query))[1][:-1])
    movies_only = [m for m in movies['d'] if m.get('q') is not None and m['q'] == 'feature']
    return json({'data': movies_only})


@imdbBlueprint.route('/popular/', methods=['GET', 'OPTIONS'])
@doc.summary('Most popular movies')
@doc.description('Gets the most popular movies at time of request')
@doc.consumes(None)
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
