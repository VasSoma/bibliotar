
from ...extensions import db
from .schemas import UserResponseSchema
from ...models import *
from sqlalchemy import select


class UserService:
    @staticmethod
    def user_registrate(request):
        try:
            if db.session.execute(select(user).filter_by(email = request["email"])).scalar_one_or_none():
                return False, "E-mail alredy exist!"
            request["address"] = home_address(**request["address"])
            user = user(**request)
            user.set_password(user.password)
            # user.roles.append(db.session.execute(select(Role).filter_by(name="User")).scalar_one())
            db.session.add(user)
            db.session.commit()
            return True, UserResponseSchema().dump(user)
        except Exception as e:
            return False, f"Incorrect user data! : {e}"

    @staticmethod
    def user_login(query):
        pass