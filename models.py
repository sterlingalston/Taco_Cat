import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('taco_cat.db')

class User(UserMixin, Model):
    email = CharField(unique = True)
    password = CharField(max_length = 100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
    
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
    user = ForeignKeyField(
        rel_model = User,
        related_name = 'tacos'
    )
    
    protein = CharField(max_length = 100)
    shell = CharField(max_length = 100)
    cheese = BooleanField(default = False)
    extras = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)    
    
    
def initialize():
    DATABASE.connect()
    # for some reason need to build tables in separate calls -- don't know why
    DATABASE.create_tables([User], safe=True)
    DATABASE.create_tables([Taco], safe=True)
    DATABASE.close()