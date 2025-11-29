from app.model.kategori import Kategori
from app import app, response, db
from flask import request, jsonify, session, render_template, redirect, url_for, flash

def saveKategori():
    nama_kategori = request.form['nama_kategori']
    if not nama_kategori:
        flash('Nama kategori harus diisi!', 'danger')
        return redirect(url_for('category'))
    
    kategoris = Kategori(nama_kategori=nama_kategori)
    try:
        db.session.add(kategoris)
        db.session.commit()
        flash('Kategori berhasil ditambahkan!', 'success')
    except Exception as e:
        flash(f'Gagal menambahkan kategori: {str(e)}', 'danger')
    return redirect(url_for('category'))
        
def updateKategori(id):
    kategori = Kategori.query.get_or_404(id)
    nama_kategori = request.form.get('nama_kategori')
    if not nama_kategori:
        flash('Nama kategori tidak boleh kosong!', 'danger')
        return redirect(url_for('category'))
    
    kategori.nama_kategori = nama_kategori
    try:
        db.session.commit()
        flash('Kategori berhasil diperbarui!', 'success')
    except Exception as e:
        flash(f'Gagal memperbarui kategori: {str(e)}', 'danger')
    return redirect(url_for('category'))

        
def deleteKategori(id):
    kategori = Kategori.query.get_or_404(id)
    try:
        db.session.delete(kategori)
        db.session.commit()
        flash('Kategori berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus kategori: {str(e)}', 'danger')
    return redirect(url_for('category'))

