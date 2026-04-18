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
            user = db.session.execute(
                select(User).filter_by(user_id=user_id)
            ).scalar_one_or_none()
            if not user:
                return False, "User not found"

            user.name = data["name"]
            user.email = data["email"]
            user.phone_number = data["phone_number"]

            if user.addresses:
                address = user.addresses[0]
                for key, value in data["address"].items():
                    setattr(address, key, value)
            else:
                address = Home_address(**data["address"])
                user.addresses.append(address)

            db.session.commit()

            addr = user.addresses[0]
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
                }
            }
        except Exception as e:
            db.session.rollback()
            return False, f"Profile update failed: {e}"
