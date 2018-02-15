from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc

from apitanic.controller.imdb import imdbBlueprint
from apitanic.controller.user import userBlueprint
from apitanic.controller.favourites import favBlueprint
from apitanic.controller.friends import friendsBlueprint
from apitanic.controller.recommendations import recommendationsBlueprint


application = app = Sanic(strict_slashes=True)

application.config.API_VERSION = '0.5.0'
application.config.API_TITLE = 'ApiTanic'
application.config.API_DESCRIPTION = 'IMDB movie info with favourites and recommendations'
application.config.API_TERMS_OF_SERVICE = 'See License'
application.config.API_PRODUCES_CONTENT_TYPES = ['application/json']
application.config.API_CONTACT_EMAIL = 'apitanic@example.com'

application.blueprint(userBlueprint)
application.blueprint(imdbBlueprint)
application.blueprint(favBlueprint)
application.blueprint(friendsBlueprint)
application.blueprint(recommendationsBlueprint)

application.blueprint(openapi_blueprint)
application.blueprint(swagger_blueprint)


@application.route("/", methods=['GET', 'OPTIONS'])
@doc.summary("Simple hello")
@doc.description("Simple hello world request")
@doc.produces({"success": str, "name": str, "tagline": str, "tagline2": str, "AKA": list})
async def test(request):
    return json({
        'success': True,
        'name': 'API Tanic',
        'tagline': 'The API that never goes down',
        'tagline2': 'always asyncs',
        'AKA': [
            'Planet of the API\'s',
            'Life of API',
            'Snakes on an API',
            'Lord of APIs',
            'Cloudy with a change of APIs'
        ]
    })


if __name__ == "__main__":
    application.run(port=8000)
