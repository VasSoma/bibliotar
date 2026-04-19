import os

def load_private_key():
    key_path = os.path.join(os.path.dirname(__file__), ".ssh", "private-key.pem")
    with open(key_path, 'r') as f:
        return f.read()

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres.audkhglijhnoiikgqrgj:Bibliotar123?@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = load_private_key()
    JWT_EXPIRATION_MINUTES = 30
