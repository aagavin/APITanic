from apitanic.model.firebase import Firebase
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic_openapi import doc

friendsBlueprint = Blueprint('friends', url_prefix='friends')
firebase = Firebase()


class FriendsController(HTTPMethodView):

    @doc.summary('')
    async def get(self, request: Request):
        pass

    @doc.summary('Add a new friend')
    @doc.description('Add a new friend to the list of friends')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes({'friendId': str}, location='body')
    async def post(self, request: Request):
        token = request.headers['token']

    async def delete(self, request: Request):
        pass


friendsBlueprint.add_route(FriendsController.as_view(), '/')
