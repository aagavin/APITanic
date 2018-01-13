from apitanic.model.friends import Friends
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic_openapi import doc

friendsBlueprint = Blueprint('friends', url_prefix='friends')
friends = Friends()


class FriendsController(HTTPMethodView):

    @doc.summary('')
    async def get(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        firends = await friends.get_all_friends(token)
        return json({'data': {'friends': firends}})

    @doc.summary('Add a new friend')
    @doc.description('Add a new friend to the list of friends')
    @doc.consumes({'token': str}, location='header')
    @doc.consumes({'friendId': str}, location='body')
    async def post(self, request: Request):
        token = request.headers['token']
        friend_id = request.json['friend_id']
        added = await friends.add_friend(token, friend_id)
        if not added:
            return json({'error': 'Error with adding friend'})
        return json({'data': 'success'})

    @doc.summary('')
    @doc.description('')
    @doc.consumes('')
    @doc.produces('')
    async def delete(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        friend_id = request.headers['friend_id']
        await friends.delete_friend(token, friend_id)
        return json({'data': 'success'})


friendsBlueprint.add_route(FriendsController.as_view(), '/')
