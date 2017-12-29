from apitanic.controller.imdb import imdbBlueprint
from apitanic.controller.auth import userBlueprint
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin


app = Sanic()
app.blueprint(userBlueprint)
app.blueprint(imdbBlueprint)
cors = CORS(app, resources=***REMOVED***"*": ***REMOVED***"origins": "*"***REMOVED******REMOVED***)


# py2swagger falcon apitanic.main:app


@app.route("/")
async def test(request):
    return json(***REMOVED***
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
            ***REMOVED***)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
