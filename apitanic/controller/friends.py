from typing import List
from apitanic.model.firebase import Firebase
from sanic import Blueprint
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from ..model.user import UserSchema

favBlueprint = Blueprint('friends', url_prefix='friends')
firebase = Firebase()


class FriendsController(HTTPMethodView):

    @doc.summary('Gets a users friends')
    @doc.description('With the token in the header returns list of friends')
    @doc.consumes({"token": str}, location='header')
    @doc.produces({'data': {'friends': List[str]}})
    async def get(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        friends = firebase.get_user_by_id(token).friends
        return json({'data': {'friends': friends}})

    @doc.summary('Adds a new favourite')
    @doc.description('Adds a new favourite to a users list of favourite')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes('user_id', location='body')
    @doc.consumes('friend_id', location='body')
    @doc.produces({'data': {'success': bool}})
    async def post(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        user_id = request.json['user_id']
        friend_id = request.json['friend_id']
        added = firebase.add_friend(token, user_id, friend_id)
        if not added:
            return json({'data': {'success': False, 'message': 'friend already added'}})
        return json({'data': {'success': True}})

   