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
    async def get(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        firends = firebase.get_all_friends(token)
        return json({'data': {'friends': firends}})

    @doc.summary('Add a new friend')
    @doc.description('Add a new friend to the list of friends')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes({'friendId': str}, location='body')
    async def post(self, request: Request):
        token = request.headers['token']
        friend_id = request.json['friend_id']
        added = firebase.add_friend(token, friend_id)
        if not added:
            return json({'error': 'Error with adding friend'})
        return json({'data': 'success'})

    async def delete(self, request: Request) -> HTTPResponse:
        pass


friendsBlueprint.add_route(FriendsController.as_view(), '/')
