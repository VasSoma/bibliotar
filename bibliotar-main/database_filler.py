from flask import Flask
from config import Config
from backend import create_app

from backend import db


################################    ROLE    UPDATE  ########################################
from backend.models.role import Role
from backend.models.user import User, UserRole
from backend.models.home_address import Home_address

app = create_app(config_class=Config) 
app.app_context().push() #FLASK main

db.session.add_all([Role(role_name="Administrator"),
                    Role(role_name="Librarian"),
                    Role(role_name="User")])
db.session.commit()

# if __name__ =="__main__":
#     create_app(config_class=Config).run('localhost',8888) 