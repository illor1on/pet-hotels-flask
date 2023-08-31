from flask_sqlalchemy import SQLAlchemy
from main import app
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import sha512_crypt



db = SQLAlchemy(app)



class Hotel(db.Model):
    __tablename__ = "Hotel"

    id = db.Column(db.Integer, primary_key=True, autoincrement='ignore_fk')
    name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    countOfPlaces = db.Column(db.Integer)
    adress = db.Column(db.String(1000))
    timezone = db.Column(db.String(10))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    owner_id = db.Column(db.Integer)


    def __init__(self, name, city, countOfPlaces, adress, timezone, email, phone, owner_id):
            self.name = name
            self.city = city
            self.countOfPlaces = countOfPlaces
            self.adress = adress
            self.timezone = timezone
            self.email = email
            self.phone = phone
            self.owner_id = owner_id
    '''def __repr__(self):
        d = "{0},{1},{2},{3},{4},{5}".format(self.name, self.city, str(self.countOfPlaces), self.timezone, self.email, str(self.phone))           return d'''


class Room(db.Model):
    __tablename__ = "Room"

    room_id = db.Column(db.Integer(), primary_key=True)
    hotel_id = db.Column(db.Integer())
    room_name = db.Column(db.String(255))
    places = db.Column(db.Integer())
    description = db.Column(db.String(2047))
    services = db.Column(db.String(255))
    photoes = db.Column(db.String(2047))

    def __init__(self, hotel_id, room_name, places, description, services, photoes):
        self.room_name = room_name
        self.hotel_id = hotel_id
        self.places = places
        self.description = description
        self.services = services
        self.photoes = photoes


class Ways(db.Model):
    __tablename__ = "PopularRoutes"
    way_id = db.Column(db.Integer(), primary_key=True)
    way_name = db.Column(db.String(255))
    way_description = db.Column(db.String(1023))
    photo_url = db.Column(db.String(1023))


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, **kwargs):
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.phone = kwargs.get('phone')
        self.email = kwargs.get('email')
        self.password = sha512_crypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not sha512_crypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user




class PassportData(db.Model):
    __tablename__ = "PassportData"

    id = db.Column(db.Integer(), primary_key=True, autoincrement='ignore_fk')
    user_id = db.Column(db.Integer())
    number = db.Column(db.String(255))
    series = db.Column(db.Integer())
    date = db.Column(db.String(255))
    gov = db.Column(db.String(255))


class CardData(db.Model):
    __tablename__ = "CardData"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    holder_name = db.Column(db.String(255))
    num = db.String(db.String(16))
    cvv = db.String(db.String(3))
    month = db.String(db.String(2))
    year = db.String(db.String(2))


class BookData(db.Model):
    __tablename__ = "Available"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    room_id = db.Column(db.Integer())
    date_from = db.Column(db.Date())
    date_to = db.Column(db.Date())

    def __init__(self, user_id, room_id, date_from, date_to):
        self.user_id = user_id
        self.room_id = room_id
        self.date_from = date_from
        self.date_to = date_to