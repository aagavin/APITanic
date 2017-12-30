from apitanic.model.firebase import Firebase
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc


userBlueprint = Blueprint('user', url_prefix='user')
firebase = Firebase()


@userBlueprint.route('/create/', methods=['POST'])
@doc.summary("Create a new account")
@doc.consumes({"user": str, "displayName": str, "email": str}, location="body")
@doc.produces({'data': {'token': str}})
async def create_accoutn(request: Request):
    token = firebase.create_account(
        request.json['email'],
        request.json['password'],
        request.json['displayName']
    )
    return json({
        'data': {'token': token}
    })
