from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    friends = fields.List(fields.Str())
    favourites = fields.List(fields.Str())
