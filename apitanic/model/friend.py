from marshmallow import Schema, fields


class FriendSchema(Schema):
    friend_id = fields.Str()
    user_id = fields.Str()
