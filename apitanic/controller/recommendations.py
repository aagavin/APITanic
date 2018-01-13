from apitanic.model.firebase import Firebase
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc


recommendationsBlueprint = Blueprint('recommendations', url_prefix='recommendations')
firebase = Firebase()


@recommendationsBlueprint.route('/')
@doc.summary('Gets a list of favourites')
@doc.description('With token in header get a list of recommendations')
@doc.consumes({'token': str}, location='header')
@doc.produces('')
async def get(request: Request) -> HTTPResponse:
    token = request.headers['token']
    recommendations = await firebase.get_recommendations(token)
    return json({'data': {'recommendations': recommendations}})
