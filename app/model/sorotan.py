from app import db
from datetime import datetime

class Sorotan(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_sorotan = db.Column(db.String(250), nullable=False)
    gambar_sorotan = db.Column(db.String(500), nullable=False)
    waktu_sorotan = db.Column(db.Integer, nullable=False)
    kategori_id = db.Column(db.BigInteger, db.ForeignKey('kategori.id'), nullable=False)
    deskripsi_sorotan = db.Column(db.Text, nullable=False)
    alat_sorotan = db.Column(db.Text, nullable=False)
    langkah_sorotan = db.Column(db.Text, nullable=False)
    penulis = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    kategori = db.relationship('Kategori', backref=db.backref('sorotan', lazy=True))
    pembuat = db.relationship('User', backref=db.backref('sorotan', lazy=True))

    def __repr__(self):
        return "<Sorotan {} - {}>".format(self.id, self.nama_sorotan)
