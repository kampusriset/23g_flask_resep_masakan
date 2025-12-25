import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = os.environ.get("DB_HOST", "127.0.0.1")
    PORT = os.environ.get("DB_PORT", "3306")  
    DATABASE = os.environ.get("DB_DATABASE", "cookify")
    USERNAME = os.environ.get("DB_USERNAME", "root")
    PASSWORD = os.environ.get("DB_PASSWORD", "")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'cookify.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')