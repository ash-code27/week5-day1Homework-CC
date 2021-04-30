from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for Secrets Module (Provided by Python)
import secrets 

# Imports for Login Manager and the UserMixin
from flask_login import LoginManager, UserMixin

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model,UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)
    
    def __init__(self, email, name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.name = name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

        

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    year = db.Column(db.String(150))
    make = db.Column(db.String(200), nullable = True)
    model = db.Column(db.String(200))
    transmission = db.Column(db.String(200))
    color = db.Column(db.String(150))
    date_created = date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)




    def __init__(self,year, make, model, transmission, color, user_token, id = ''):
        self.id = self.set_id()
        self.year = year
        self.make = make
        self.model = model
        self.transmission = transmission
        self.color = color
        self.user_token = user_token


    def __repr__(self):
        return f'The following Car has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()


# Creation of API Schema via the marshmallow package
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'year', 'make', 'model', 'transmission', 'color']



car_schema = CarSchema()
cars_schema = CarSchema(many = True)




