from apitanic.model.user import User
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic_openapi import doc


userBlueprint = Blueprint('user', url_prefix='user')
userModel = User()


class UserController(HTTPMethodView):

    @doc.summary('Search user')
    @doc.description('Using the query string q search db for user name and password')
    @doc.consumes('q', location='query')
    @doc.produces({'data': {'results': list}})
    async def get(self, request: Request)-> HTTPResponse:
        token = request.headers.get('token')
        user = await userModel.get_user_id_by_token(token)
        if user is None:
            return json({'error': 'token not valid'})
        query_string = request.args['q'][0]
        results = await userModel.search_user(query_string.lower())
        return json({'data': {'results': results}})

    @doc.summary('Create a new account')
    @doc.consumes({'user': str, 'displayName': str, 'email': str}, location='body')
    @doc.description('Create a user account and returns a token')
    @doc.produces({'data': {'token': str}})
    async def post(self, request: Request):
        token = userModel.create_account(
            request.json['email'],
            request.json['password'],
            request.json['displayName']
        )
        return json({'data': {'token': token}})


userBlueprint.add_route(UserController.as_view(), '/')
