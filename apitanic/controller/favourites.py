from typing import List
from apitanic.model.firebase import Firebase
from sanic import Blueprint
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from ..model.favourites import FavouritesSchema

favBlueprint = Blueprint('favourites', url_prefix='favourites')
firebase = Firebase()


class FavouritesController(HTTPMethodView):

    @doc.summary('Gets a users favourites')
    @doc.description('With the token in the header returns list of favourites')
    @doc.consumes({"token": str}, location='header')
    @doc.produces({'data': {'favourites': List[FavouritesSchema]}})
    async def get(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        favourites = firebase.get_all_favourites(token)
        return json({'data': {'favourites': favourites}})

    @doc.summary('Adds a new favourite')
    @doc.description('Adds a new favourite to a users list of favourite')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes(FavouritesSchema, location='body')
    @doc.produces({'data': {'success': bool}})
    async def post(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        imdbId = request.json['imdbId']
        added = firebase.add_favourite(token, imdbId)
        if not added:
            return json({'data': {'success': False, 'message': 'favourite already added'}})
        return json({'data': {'success': True}})

    @doc.summary('Remove a favourite')
    @doc.description('Remove a user favourite')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes(FavouritesSchema, location='body')
    @doc.produces({'data': {'success': bool}})
    async def delete(self, request) -> HTTPResponse:
        token = request.headers['token']
        imdb_id = request.json['imdbId']
        firebase.delete_favourite(token, imdb_id)
        return json({'data': {'success': True}})


favBlueprint.add_route(FavouritesController.as_view(), '/')
