from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): #default class, work with instantiation 
    pass

db = SQLAlchemy(model_class = Base) # given to sqlalchemy