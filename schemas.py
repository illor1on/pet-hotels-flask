from marshmallow import Schema, validate, fields


class HotelSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=255)])
    city = fields.String(required=True, validate=[validate.Length(max=255)])
    countOfPlaces = fields.Integer(required=True)
    adress = fields.String(required=True, validate=[validate.Length(max=1000)])
    timezone = fields.String(required=True, validate=[validate.Length(max=10)])
    email = fields.String(required=True, validate=[validate.Length(max=255)])
    phone = fields.String(required=True, validate=[validate.Length(max=50)])
    owner_id = fields.Integer(required=True)


class RoomSchema(Schema):
    room_id = fields.Integer(dump_only=True)
    hotel_id = fields.Integer(dump_only=True)
    room_name = fields.String(required=True, validate=[validate.Length(max=255)])
    places = fields.Integer(required=True)
    description = fields.String(required=True, validate=[validate.Length(max=2047)])
    services = fields.String(required=True, validate=[validate.Length(max=255)])
    photoes = fields.String(required=True, validate=[validate.Length(max=2047)])


class WaySchemas(Schema):
    way_id = fields.Integer(dump_only=True)
    way_name = fields.String(required=True, validate=[validate.Length(max=255)])
    way_description = fields.String(required=True, validate=[validate.Length(max=1023)])
    photo_url = fields.String(required=True, validate=[validate.Length(max=1023)])


class PassportSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    number = fields.String(required=True, validate=[validate.Length(max=255)])
    series = fields.Integer(required=True)
    date = fields.String(required=True, validate=[validate.Length(max=255)])
    gov = fields.String(required=True, validate=[validate.Length(max=255)])


class CardSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    holder_name = fields.String(required=True, validate=[validate.Length(max=255)])
    num = fields.String(required=True, validate=[validate.Length(max=16)])
    cvv = fields.String(required=True, validate=[validate.Length(max=3)])
    month = fields.String(required=True, validate=[validate.Length(max=2)])
    year = fields.String(required=True, validate=[validate.Length(max=2)])


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    #hotel_id = fields.Integer(required=True)
    room_id = fields.Integer(required=True)
    date_from = fields.String(required=True, validate=[validate.Length(max=255)])
    date_to = fields.String(required=True, validate=[validate.Length(max=255)])