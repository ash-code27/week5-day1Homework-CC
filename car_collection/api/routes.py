from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required
from car_collection.models import User, Car, car_schema, car_schema, db

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'some':'value'}

# CREATE CAR ENDPOINT
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    type = request.json['type'] 
    color = request.json['color'] 
    user_token = current_user_token.token

    car = Car(year, make, model, type, color, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)


# RETRIEVE ALL CHARACTERS ENDPOINT
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

     
    
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    character = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# UPDATE CAR ENDPOINT
@api.route('/cars/<id>', methods = [ 'POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id) #Getting a car instance

    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    car.type = request.json['type']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# DELETE CAR ENDPOINT
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)