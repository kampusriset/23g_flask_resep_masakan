import os
from werkzeug.utils import secure_filename
from app.model.sorotan import Sorotan
from app.model.kategori import Kategori
from app.model.user import User
from app import app, response, db
from flask import request, jsonify, session, render_template, redirect, url_for, flash

UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])  

def saveSorotan():
    try:
        existing_sorotan = Sorotan.query.first()  # Ganti 'Sorotan' dengan model yang sesuai
        if existing_sorotan:
            flash("Sorotan hanya dapat ditambahkan satu kali.", "danger")
            return redirect(url_for('dashboard'))
        
        nama_sorotan = request.form.get('nama_sorotan')
        waktu_sorotan = request.form.get('waktu_sorotan')
        deskripsi_sorotan = request.form.get('deskripsi_sorotan')
        alat_sorotan = request.form.get('alat_sorotan')
        langkah_sorotan = request.form.get('langkah_sorotan')
        kategori_id = int(request.form.get('kategori_id'))
        
        
        # Validasi file gambar
        file = request.files.get('gambar_sorotan')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
            file.save(filepath)
        else:
            filepath = None

        # Tambah resep
        sorotan = Sorotan(
            nama_sorotan=nama_sorotan,
            waktu_sorotan=waktu_sorotan,
            deskripsi_sorotan=deskripsi_sorotan,
            alat_sorotan=alat_sorotan,
            langkah_sorotan=langkah_sorotan,
            kategori_id=kategori_id,
            gambar_sorotan=filepath,
            penulis=session.get('user_id')
        )
        db.session.add(sorotan)
        db.session.commit()
        flash('Data Sorotan berhasil ditambahkan!', 'success')
    except Exception as e:
        flash(f'Gagal menyimpan sorotan: {str(e)}', 'danger')
    return redirect(url_for('sorotan'))


def updateSorotan(id):
    sorotan = Sorotan.query.get_or_404(id)
    try:
        # Perbarui data dari form
        sorotan.nama_sorotan = request.form.get('nama_sorotan')
        sorotan.waktu_sorotan = request.form.get('waktu_sorotan')
        sorotan.deskripsi_sorotan = request.form.get('deskripsi_sorotan')
        sorotan.alat_sorotan = request.form.get('alat_sorotan')
        sorotan.langkah_sorotan = request.form.get('langkah_sorotan')
        sorotan.kategori_id = int(request.form.get('kategori_id'))

        # Update gambar jika ada file baru
        file = request.files.get('gambar_sorotan')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
            file.save(filepath)
            sorotan.gambar = filepath

        db.session.commit()
        flash('Sorotan berhasil diperbarui!', 'success')
    except Exception as e:
        flash(f'Gagal memperbarui sorotan: {str(e)}', 'danger')
    return redirect(url_for('sorotan'))


def deleteSorotan(id):
    sorotan = Sorotan.query.get_or_404(id)
    try:
        # Hapus file gambar jika ada
        if sorotan.gambar and os.path.exists(sorotan.gambar):
            os.remove(sorotan.gambar)
        db.session.delete(sorotan)
        db.session.commit()
        flash('Sorotan berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus sorotan: {str(e)}', 'danger')
    return redirect(url_for('sorotan'))

def index():
    try:
        # Mengambil data resep dari database
        sorotan_list = Sorotan.query.all()
        sorotan_data = [
            {
                'id': sorotan.id,
                'nama_sorotan': sorotan.nama_sorotan,
                'waktu_sorotan': sorotan.waktu_sorotan,
                'deskripsi_sorotan': sorotan.deskripsi_sorotan,
                'gambar': sorotan.gambar_sorotan,
                'oleh': User.query.get(sorotan.penulis).nama if sorotan.penulis else 'Anonim'
            } for sorotan in sorotan_list
        ]
        # Render template dengan data resep
        return render_template('pages/home.html', sorotan_data=sorotan_data)
    except Exception as e:
        flash(f'Gagal memuat data sorotan: {str(e)}', 'danger')
        return render_template('pages/home.html', sorotan_data=[])