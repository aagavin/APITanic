from typing import List
from apitanic.model.user import User
from apitanic.model.favourites import Favourites
from sanic import Blueprint
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_openapi import doc


favBlueprint = Blueprint('favourites', url_prefix='favourites')
favourites = Favourites()
user = User()


class FavouritesController(HTTPMethodView):

    @staticmethod
    async def get_by_id(request: Request, imdbid: str) -> HTTPResponse:
        token = request.headers['token']
        user_id = await user.get_user_id_by_token(token)
        fav = []
        fav_ref = await favourites.get_favoutie_by_id(user_id, imdbid)
        for f in fav_ref:
            fav.append(f.to_dict())
        print(fav)
        return json({'data': {'favourite': fav}})

    @doc.summary('Gets a users favourites')
    @doc.description('With the token in the header returns list of favourites')
    @doc.consumes({'token': str}, location='header')
    @doc.produces({'data': {'favourites': List[dict]}})
    async def get(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        favs = await favourites.get_all_favourites(token)
        return json({'data': {'favourites': favs}})

    @doc.summary('Adds a new favourite')
    @doc.description('Adds a new favourite to a users list of favourite')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes(dict, location='body')
    @doc.produces({'data': {'success': bool}})
    async def post(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        imdbId = request.json['imdbId']
        added = await favourites.add_favourite(token, imdbId)
        if not added:
            return json({'data': {'success': False, 'message': 'favourite already added'}})
        return json({'data': {'success': True}})

    @doc.summary('Remove a favourite')
    @doc.description('Remove a user favourite')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes(dict, location='body')
    @doc.produces({'data': {'success': bool}})
    async def delete(self, request) -> HTTPResponse:
        token = request.headers['token']
        imdb_id = request.headers['imdbId']
        await favourites.delete_favourite(token, imdb_id)
        return json({'data': {'success': True}})


favBlueprint.add_route(FavouritesController.as_view(), '/')
favBlueprint.add_route(FavouritesController.get_by_id, '/<imdbid>')
