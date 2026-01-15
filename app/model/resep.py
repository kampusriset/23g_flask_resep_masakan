from app import db
from datetime import datetime

class Resep(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_resep = db.Column(db.String(250), nullable=False)
    gambar = db.Column(db.String(500), nullable=False)
    waktu_masak = db.Column(db.Integer, nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=False)
    deskripsi_singkat = db.Column(db.Text, nullable=False)
    alat_dan_bahan = db.Column(db.Text, nullable=False)
    langkah_langkah = db.Column(db.Text, nullable=False)
    dibuat_oleh = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_top_pick = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    kategori = db.relationship('Kategori', backref=db.backref('resep', lazy=True))
    pembuat = db.relationship('User', backref=db.backref('resep', lazy=True))

    def __repr__(self):
        return "<Resep {} - {}>".format(self.id, self.nama_resep)
