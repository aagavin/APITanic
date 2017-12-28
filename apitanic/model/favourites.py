from marshmallow import Schema, fields


class FavouritesSchema(Schema):
    imbdId = fields.Str()
    userId = fields.Str()
