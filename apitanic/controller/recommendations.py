from apitanic.model.firebase import Firebase
from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic_openapi import doc


recommendationsBlueprint = Blueprint('recommendations', url_prefix='recommendations')
firebase = Firebase()


class Recommendations(HTTPMethodView):

    @doc.summary('Gets a list of favourites')
    @doc.description('With token in header get a list of recommendations')
    @doc.consumes({'token': str}, location='header')
    @doc.produces('')
    async def get(self, request: Request) -> HTTPResponse:
        token = request.headers['token']
        await firebase.get_recommendations(token)
        return json({'data': True})


recommendationsBlueprint.add_route(Recommendations.as_view(), '/')
