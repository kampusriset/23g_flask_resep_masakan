from app import db
from datetime import datetime

class Kategori(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_kategori = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<Kategori {}>".format(self.id)

    