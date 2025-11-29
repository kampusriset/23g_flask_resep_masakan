from flask import jsonify, request, redirect, url_for, session, flash
from app.decorators import login_required
from app import db  # Pastikan ini disesuaikan dengan struktur proyek Anda
from app.model.favorit import Favorit

def tambahFavorit(resep_id):
    # Periksa apakah pengguna login berdasarkan session
    if 'user_id' not in session:  # Misalnya user_id disimpan di session setelah login
        flash('Silakan login untuk mengakses halaman ini', 'warning')
        return redirect(url_for('login'))  # Arahkan ke halaman login jika belum login

    user_id = session['user_id']  # Dapatkan ID pengguna dari session

    # Cek apakah resep sudah ada di favorit
    favorit = Favorit.query.filter_by(user_id=user_id, resep_id=resep_id).first()
    if favorit:
        return jsonify({'message': 'Resep sudah ada di favorit'}), 400

    try:
        # Tambahkan resep ke favorit
        new_favorit = Favorit(user_id=user_id, resep_id=resep_id)
        db.session.add(new_favorit)
        db.session.commit()
        return jsonify({'message': 'Resep berhasil ditambahkan ke favorit'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Terjadi kesalahan'}), 500
    
def hapusFavorit(resep_id):
    # Pastikan pengguna sudah login
    if 'user_id' not in session:  # Misalnya user_id disimpan di session setelah login
        flash('Silakan login untuk mengakses halaman ini', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']  # Dapatkan ID pengguna dari session

    # Cari favorit berdasarkan user_id dan resep_id
    favorit = Favorit.query.filter_by(user_id=user_id, resep_id=resep_id).first()
    if not favorit:
        return jsonify({'message': 'Favorit tidak ditemukan'}), 404

    try:
        # Hapus data favorit dari database
        db.session.delete(favorit)
        db.session.commit()
        return jsonify({'message': 'Favorit berhasil dihapus'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Terjadi kesalahan'}), 500