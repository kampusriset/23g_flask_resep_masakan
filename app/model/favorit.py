from app import db
from datetime import datetime

class Favorit(db.Model):
    __tablename__ = 'favorit'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    resep_id = db.Column(db.BigInteger, db.ForeignKey('resep.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('favorits', lazy='dynamic'))
    resep = db.relationship('Resep', backref=db.backref('favorits', lazy='dynamic'))

    def __repr__(self):
        return f"<Favorit User: {self.user_id}, Resep: {self.resep_id}>" 
