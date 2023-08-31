from flask import Flask, request
from flask import jsonify
from geopy.geocoders import Nominatim
from flask_migrate import Migrate, MigrateCommand
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import *
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from sqlalchemy import create_engine, and_, func, or_
from models import *
from config import Config
from flask_script import Manager
from datetime import datetime



app = Flask(__name__)

app.config.from_object(Config)

docs = FlaskApiSpec()

jwt = JWTManager(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.config['JSON_AS_ASCII'] = False

docs.init_app(app)

app.config.update({
    'API_SPEC': APISpec(
        title='hws',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL':'/swagger/'
})

engine = create_engine('postgresql://postgres:1922@localhost:5432/BAR_proj')




dev = True

if dev == True:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1922@localhost:5432/BAR_proj'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bqsrbqvcvmhlil:ba3d16987ec8f29e9bee7deafa06fc5558a445768b6321e73e5e5a11c50d4f24@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/d8pn9aeiiatqrl'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Регистрация в сервисе
@app.route("/register", methods=['POST'])
def register():
    params = request.get_json()
    user = User(**params)
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    return {'token ': token}


#Авторизация в сервисе
@app.route("/login", methods=['POST'])
def login():
    params = request.get_json()
    user = User.authenticate(**params)
    token = user.get_token()
    return {'token ': token}


#Получение направлений поездки(Города, курорты)
@app.route("/", methods=["GET"])
def get_ways():
    way = db.session.query(Ways).all()
    schema = WaySchemas(many=True)
    return jsonify(schema.dump(way))


#Получение всех отелей из БД
@app.route("/hotels", methods=['GET'])
def get_hotels():
    hotels = db.session.query(Hotel).all()
    schema = HotelSchema(many=True)
    return jsonify(schema.dump(hotels))


#!!!Получение номерного фонда отеля по id отеля
@app.route("/hotels/<int:hotel_id>", methods=["GET"])
def get_hotel(hotel_id):
    rooms = db.session.query(Room).filter(Room.hotel_id == hotel_id)
    schema = RoomSchema(many=True)
    return jsonify(schema.dump(rooms))


'''#Добавление отеля в БД
@app.route("/hotels/add-object", methods=['POST'])
@jwt_required()
@use_kwargs(HotelSchema)
@marshal_with(HotelSchema)
def add_object(**kwargs):
    hotel = Hotel(**kwargs)
    db.session.add(hotel)
    db.session.commit()
    user_id = get_jwt_identity()
    print(user_id)
    #return 'ok'
    return str(user_id)'''


#Добавление отеля в БД
@app.route("/hotels/add-object", methods=['POST'])
@jwt_required()
def add_object():
    data = request.get_json()
    name = data['name']
    city = data['city']
    countOfPlaces = data['countOfPlaces']
    adress = data['adress']
    timezone = data['timezone']
    email = data['email']
    phone = data['phone']
    owner_id = get_jwt_identity()
    hotel = Hotel(name=name, city=city, countOfPlaces=countOfPlaces, adress=adress, timezone=timezone, email=email, phone=phone, owner_id=owner_id)
    db.session.add(hotel)
    db.session.commit()
    return 'ok'


#Добавление номера в отель
@app.route("/hotels/<int:hotel_id>", methods=['POST'])
@jwt_required()
def add_room(hotel_id):
    data = request.get_json()
    name = data['name']
    places = data['places']
    description = data['description']
    services = data['services']
    photoes = data['photos']
    user_id = get_jwt_identity()
    hotel_owner_id = db.session.query(Hotel.owner_id).filter(Hotel.id == hotel_id)
    if user_id == hotel_owner_id[0][0]:
        room = Room(room_name=name, hotel_id=hotel_id, places=places, description=description, services=services, photoes=photoes)
        db.session.add(room)
        db.session.commit()
        return 'ok'
    return 'error'


#добавление паспорта
@app.route("/add-passport", methods=["POST"])
@jwt_required()
@use_kwargs(PassportSchema)
@marshal_with(PassportSchema)
def add_passport(**kwargs):
    passport = PassportData(**kwargs)
    db.session.add(passport)
    db.session.commit()
    return passport


#Проверить доступность номеров в пределах заданных дат
@app.route('/book/<int:room_id>', methods=['GET'])
def check_book(room_id):
    dateformat = "%Y-%m-%d"
    dates = request.get_json()
    date_from = dates['date_from']
    date_to = dates['date_to']
    date_from = datetime.strptime(date_from, dateformat)
    date_to = datetime.strptime(date_to, dateformat)
    schema = BookSchema(many=True)
    bookings = db.session.query(BookData).filter(and_((BookData.room_id==room_id), (or_(func.date(BookData.date_from).between(date_from, date_to), func.date(BookData.date_to).between(date_from, date_to), and_(func.date(BookData.date_from) <= date_from, func.date(BookData.date_to) >= date_to))))).all()
    return jsonify(schema.dump(bookings))


#забронировать номер на заданные даты
@app.route('/book/<int:room_id>', methods=['POST'])
@jwt_required()
def add_book(room_id):
    user_id = get_jwt_identity()
    dateformat = "%Y-%m-%d"
    dates = request.get_json()
    date_from = dates['date_from']
    date_to = dates['date_to']
    date_from = datetime.strptime(date_from, dateformat)
    date_to = datetime.strptime(date_to, dateformat)
    bookings = db.session.query(BookData).filter(and_((BookData.room_id==room_id), (or_(func.date(BookData.date_from).between(date_from, date_to), func.date(BookData.date_to).between(date_from, date_to), and_(func.date(BookData.date_from) <= date_from, func.date(BookData.date_to) >= date_to))))).all()
    if bookings == []:
        booking = BookData(user_id=user_id, room_id=room_id, date_to=date_to, date_from=date_from)
        db.session.add(booking)
        db.session.commit()
        status = 'Забронированно'
    else:
        status = 'Номер занят'
    return status


if __name__ == "__main__":
    app.run()
