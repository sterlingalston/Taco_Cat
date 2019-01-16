import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('taco_cat.db')

class User(UserMixin, Model):
    email = CharField(unique = True)
    password = CharField(max_length = 100)
    
    @classmethod
    def create_user(cls,email, password, admin = False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email = email,
                    password = generate_password_hash(password),
                    is_admin = admin)
        except IntegrityError:
            raise ValueError("User already exists.")
            
class Taco(Model):
    user = CharField(unique = True)
    protein = CharField(max_length = 100)
    shell = CharField(max_length = 100)
    cheese = BooleanField(default = False)
    extras = TextField()
    