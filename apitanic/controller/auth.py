from apitanic.model.firebase import Firebase
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint


userBlueprint = Blueprint('user', url_prefix='user')
firebase = Firebase()


@userBlueprint.route('/create', methods=['POST'])
async def create_accoutn(request: Request):
    token = firebase.create_account(
        request.json['email'],
        request.json['password'],
        request.json['displayName']
    )
    return json({
        'data': {'token': token}
    })
