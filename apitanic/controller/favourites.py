from apitanic.model.firebase import Firebase
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc


favBlueprint = Blueprint('favourites', url_prefix='favourites')
firebase = Firebase()


@favBlueprint.route('/', methods=['GET', 'OPTIONS'])
@doc.summary("Create a new account")
@doc.description("Create a user account and returns a token")
@doc.consumes({"user": str, "displayName": str, "email": str}, location="body")
@doc.produces({'data': {'token': str}})
def get_favourites(request: Request):
    token = request.headers['token']

    firebase.get_all_favourites(token)
    return json({'hi': token+' ds'})
