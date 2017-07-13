from marshmallow import Schema, fields


class UserSchema(Schema):
    login = fields.String(required=True)
    password = fields.String(required=True)
