from typing import List
from apitanic.model.firebase import Firebase
from sanic import Blueprint
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_openapi import doc
from firebase_admin import auth

from ..model.friends import UserSchema

friendBlueprint = Blueprint('friends', url_prefix='friends')
firebase = Firebase()


class FriendsController(HTTPMethodView):

    @doc.summary('Gets a users friends')
    @doc.description('With the token in the header returns list of friends')
    @doc.consumes({"token": str}, location='header')
    @doc.produces({'data': {'friends': List[str]}})
    async def get(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        friends = firebase.get_friends(token)
        return json({'data': {'friends': friends}})

    @doc.summary('Adds a new friend')
    @doc.description('Adds a new friend to a users list of friends')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes('friend_id', location='body')
    @doc.produces({'data': {'success': bool}})
    async def post(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        friend_id = request.json['friend_id']
        added = firebase.add_friend(token, friend_id)
        if not added:
            return json({'data': {'success': False, 'message': 'friend already added'}})
        return json({'data': {'success': True}})

    @doc.summary('Remove a friend')
    @doc.description('Remove a user friend')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes('friend_id', location='body')
    @doc.produces({'data': {'success': bool}})
    async def delete(self, request) -> HTTPResponse:
        token = request.headers['token']
        friend_id = request.json['friend_id']
        firebase.delete_friend(token, friend_id)
        return json({'data': {'success': True}})

    # @doc.summary('Gets a user by email')
    # @doc.description('With the token  and email in the header returns user')
    # @doc.consumes({"token": str}, location='header')
    # @doc.consumes({'email': str}, location='header')
    # @doc.produces({'data': {'friends': List[str]}})
    # async def get(self, request: Request) -> HTTPResponse:
    #     token = request.headers['token']
    #     friend = auth.get_user_by_email(request.headers['email'])
    #     return json({'data': {'friend': friend}})


friendBlueprint.add_route(FriendsController.as_view(), '/')
