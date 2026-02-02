import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

# Pilih config berdasarkan env
if os.getenv('DB_DRIVER', 'sqlite').lower() == 'mysql':
    from mysql_config import Config as DBConfig
else:
    from config import Config as DBConfig

def strip_numbering(text):
    import re
    return re.sub(r'^[0-9]+\.?\s*', '', text.strip())

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.jinja_env.filters['strip_numbering'] = strip_numbering
    app.config.from_object(DBConfig)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return app

app = create_app()

from app.model import user, kategori, resep, sorotan, favorit
from app import routes