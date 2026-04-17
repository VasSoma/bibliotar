

class Config:
#!!!!!!!!!!!!!!!!!!!!!! TEST SERVER  !!!!!!!!!!!!!!!!!!!!!!
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.gdqijunubhvvpnqmbjkk:ParajdiSo45@aws-1-eu-west-1.pooler.supabase.com:6543/postgres' 

#!!!!!!!!!!!!!!!!!!!!!! LIVE SERVER  !!!!!!!!!!!!!!!!!!!!!!
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.audkhglijhnoiikgqrgj:Bibliotar123?@aws-1-eu-west-1.pooler.supabase.com:5432/postgres' 

    SQLALCHEMY_TRACK_MODIFICATIONS = False