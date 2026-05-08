import os

def load_private_key():
    key_path = os.path.join(os.path.dirname(__file__), ".ssh", "private-key.pem")
    with open(key_path, 'r') as f:
        return f.read()

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///mydb.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = load_private_key()
    JWT_EXPIRATION_MINUTES = 30
