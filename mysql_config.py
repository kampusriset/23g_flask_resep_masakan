import os

class Config(object):
    HOST = os.environ.get("DB_HOST", "127.0.0.1")
    PORT = os.environ.get("DB_PORT", "3306")
    DATABASE = os.environ.get("DB_DATABASE", "cookify")
    USERNAME = os.environ.get("DB_USERNAME", "root")
    PASSWORD = os.environ.get("DB_PASSWORD", "")

    # requires: pip install PyMySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
