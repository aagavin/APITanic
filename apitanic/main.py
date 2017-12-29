from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc

from apitanic.controller.imdb import imdbBlueprint
from apitanic.controller.auth import userBlueprint


app = Sanic()

app.config.API_VERSION = '0.5.0'
app.config.API_TITLE = 'ApiTanic'
app.config.API_DESCRIPTION = 'IMDB movie info with favourites and recommendations'
app.config.API_TERMS_OF_SERVICE = 'See License'
app.config.API_PRODUCES_CONTENT_TYPES = ['application/json']
app.config.API_CONTACT_EMAIL = 'apitanic@example.com'

app.blueprint(userBlueprint)
app.blueprint(imdbBlueprint)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

cors = CORS(app, resources={"*": {"origins": "*"}})


@app.route("/")
@doc.summary("Simple hello world request")
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
    app.run(port=8000)
