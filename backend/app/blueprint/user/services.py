from sqlalchemy import select
from ...extensions import db
from ...models.users import User
from ...models.home_address import Home_address


class UserService:
    @staticmethod
    def get_profile(user_id):
        try:
            user = db.session.execute(
                select(User).filter_by(user_id=user_id)
            ).scalar_one_or_none()
            if not user:
                return False, "User not found"

            addr = user.addresses[0] if user.addresses else None
            return True, {
                "user_id": user.user_id,
                "role": user.roles[0].role_name if user.roles else None,
                "name": user.name,
                "email": user.email,
                "phone_number": user.phone_number,
                "address": {
                    "county": addr.county,
                    "postal_code": addr.postal_code,
                    "city": addr.city,
                    "street": addr.street,
                    "house_number": addr.house_number
                } if addr else None
            }
        except Exception as e:
            return False, f"Failed to get profile: {e}"

    @staticmethod
    def update_profile(user_id, data):
        try:
            user = db.session.execute(select(User).filter_by(user_id=user_id)).scalar_one_or_none()
            if not user:
                return False, "User not found"

            if "name" in data:
                user.name = data["name"]
            if "email" in data:
                user.email = data["email"]
            if "phone_number" in data:
                user.phone_number = data["phone_number"]

            if "address" in data and data["address"]:
                if user.addresses:
                    for key, value in data["address"].items():
                        setattr(user.addresses[0], key, value)
                else:
                    user.addresses.append(Home_address(**data["address"]))

            db.session.commit()

            addr = user.addresses[0] if user.addresses else None
            return True, {
                "name": user.name,
                "email": user.email,
                "phone_number": user.phone_number,
                "address": {
                    "county": addr.county,
                    "postal_code": addr.postal_code,
                    "city": addr.city,
                    "street": addr.street,
                    "house_number": addr.house_number
                } if addr else None
            }
        except Exception as e:
            db.session.rollback()
            return False, f"Profile update failed: {e}"
