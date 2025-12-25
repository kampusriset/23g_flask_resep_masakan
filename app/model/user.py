from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100),  nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<User {}>".format(self.nama)
    
    def setPassword(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        
    def checkPassword(self, password):
        return check_password_hash(self.password, password)    

    
