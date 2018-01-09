from marshmallow import Schema, fields


class FriendsSchema(Schema):
    friend_id = fields.Str()
    user_id = fields.Str()

