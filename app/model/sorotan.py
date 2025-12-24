from app import db
from datetime import datetime

class Sorotan(db.Model):
    __tablename__ = 'sorotan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_sorotan = db.Column(db.String(250), nullable=False)
    gambar_sorotan = db.Column(db.String(500), nullable=False)
    waktu_sorotan = db.Column(db.Integer, nullable=False)

    kategori_id = db.Column(
        db.Integer,
        db.ForeignKey('kategori.id'),
        nullable=False
    )

    deskripsi_sorotan = db.Column(db.Text, nullable=False)
    alat_sorotan = db.Column(db.Text, nullable=False)
    langkah_sorotan = db.Column(db.Text, nullable=False)

    penulis = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    kategori = db.relationship(
        'Kategori',
        backref=db.backref('sorotan_list', lazy=True)
    )

    pembuat = db.relationship(
        'User',
        foreign_keys=[penulis],
        backref=db.backref('sorotan_list', lazy=True)
    )

    def __repr__(self):
        return f"<Sorotan {self.id} - {self.nama_sorotan}>"
