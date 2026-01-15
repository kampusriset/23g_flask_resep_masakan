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

app = Flask(__name__)
app.config.from_object(DBConfig)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.model import user, kategori, resep, sorotan, favorit
from app import routes