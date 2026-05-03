from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy import select
from authlib.jose import jwt
from ...extensions import db
from ...models.users import User
from ...models.home_address import Home_address
from ...models.role import Role
from .schemas import RoleSchema
from apiflask import HTTPError
from ...models.users import UserRole


class AuthService:
    @staticmethod
    def token_generate(user: User) -> str:
        payload = {
            "user_id": user.user_id,
            "roles": RoleSchema().dump(user.roles, many=True),
            "exp": int((datetime.now() + timedelta(minutes=current_app.config["JWT_EXPIRATION_MINUTES"])).timestamp())
        }
        return jwt.encode({'alg': 'RS256'}, payload, current_app.config['SECRET_KEY']).decode()

    @staticmethod
    def login(data):
        try:
            user = db.session.execute(
                select(User).filter_by(email=data["email"])
            ).scalar_one_or_none()

            if not user:
                return False, "Invalid email or password"

            if not user.check_password(data["password"]):
                return False, "Invalid email or password"

            token = AuthService.token_generate(user)

            return True, {
                "token": token,
                "name": user.name,
                "email": user.email
            }
        except Exception as e:
            return False, f"Login failed: {e}"

    @staticmethod
    def register(data):
        try:
            existing = db.session.execute(
                select(User).filter_by(email=data["email"])
            ).scalar_one_or_none()
            if existing:
                return False, "Email already exists"

            default_role = db.session.execute(
                select(Role).filter_by(role_id=1)
            ).scalar_one_or_none()
            if not default_role:
                return False, "Default role not found in database"

            address = Home_address(**data["address"])
            new_user = User(
                email=data["email"],
                name=data["name"],
                phone_number=data.get("phone_number"),
            )
            new_user.set_password(data["password"])
            new_user.addresses.append(address)
            new_user.roles.append(default_role)
            db.session.add(new_user)
            db.session.commit()

            return True, {
                "name": new_user.name,
                "email": new_user.email
            }
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {e}"

    @staticmethod
    def set_role(json_data):
        user = User.query.get(json_data["user_id"])
        if not user:
            raise HTTPError(404, "User not found.")

        role = Role.query.get(json_data["role_id"])
        if not role:
            raise HTTPError(404, "Role not found.")

        user.roles.append(role)
        db.session.commit()

        role_names = [role.role_name for role in user.roles]

        return {
            "user_id": user.user_id,
            "roles": role_names
        }

    @staticmethod
    def get_roles_by_user_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise HTTPError(404, "User not found.")
        return user.roles

    @staticmethod
    def get_roles():
        roles = Role.query.all()
        if not roles:
            raise HTTPError(404, "Roles table is empty.")
        return roles

    @staticmethod
    def delete_role(json_data):
        user = User.query.get(json_data["user_id"])
        if not user:
            raise HTTPError(404, "User not found.")

        role = Role.query.get(json_data["role_id"])
        if not role:
            raise HTTPError(404, "Role does not exist.")

        role_ids = [role.role_id for role in user.roles]
        if json_data["role_id"] not in role_ids:
            raise HTTPError(404, "User is not associated with the specified role.")

        role_obj = Role.query.get(json_data["role_id"])
        user.roles.remove(role_obj)
        db.session.commit()

        return "", 204