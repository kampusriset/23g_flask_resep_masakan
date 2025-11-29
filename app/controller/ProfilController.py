import os
from werkzeug.utils import secure_filename
from app.model.resep import Resep
from app.model.kategori import Kategori
from app.model.user import User
from app import app, response, db
from flask import request, jsonify, session, render_template, redirect, url_for, flash

# Path untuk menyimpan gambar
UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])  # Membuat folder jika belum ada

def tambahResep():
    try:
        nama_resep = request.form.get('nama_resep')
        waktu_masak = request.form.get('waktu_masak')
        deskripsi_singkat = request.form.get('deskripsi_singkat')
        alat_dan_bahan = request.form.get('alat_dan_bahan')
        langkah_langkah = request.form.get('langkah_langkah')
        kategori_id = int(request.form.get('kategori_id'))
        
        # Validasi file gambar
        file = request.files.get('gambar')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
            file.save(filepath)
            print(f"File saved at: {filepath}")
        else:
            print("Invalid file format or no file uploaded")
            filepath = None

        # Tambah resep
        resep = Resep(
            nama_resep=nama_resep,
            waktu_masak=waktu_masak,
            deskripsi_singkat=deskripsi_singkat,
            alat_dan_bahan=alat_dan_bahan,
            langkah_langkah=langkah_langkah,
            kategori_id=kategori_id,
            gambar=filepath,
            dibuat_oleh=session.get('user_id')
        )
        db.session.add(resep)
        db.session.commit()
        flash('Resep berhasil ditambahkan!', 'success')
    except Exception as e:
        flash(f'Gagal menyimpan resep: {str(e)}', 'danger')
    return redirect(url_for('profil'))
def editResep(id):
    resep = Resep.query.get_or_404(id)

    try:
        resep.nama_resep = request.form.get('nama_resep')
        resep.waktu_masak = request.form.get('waktu_masak')
        resep.deskripsi_singkat = request.form.get('deskripsi_singkat')
        resep.alat_dan_bahan = request.form.get('alat_dan_bahan')
        resep.langkah_langkah = request.form.get('langkah_langkah')
        resep.kategori_id = int(request.form.get('kategori_id'))

        file = request.files.get('gambar')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)

            # simpan hanya nama file
            resep.gambar = filename

        db.session.commit()
        flash('Resep berhasil diperbarui!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui resep: {str(e)}', 'danger')

    return redirect(url_for('profil'))

def hapusResep(id):
    resep = Resep.query.get_or_404(id)
    try:
        # Hapus file gambar jika ada
        if resep.gambar and os.path.exists(resep.gambar):
            os.remove(resep.gambar)
        db.session.delete(resep)
        db.session.commit()
        flash('Resep berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus resep: {str(e)}', 'danger')
    return redirect(url_for('profil'))

def tampilResep():
    try:
        # Mengambil data resep dari database
        resep_list = Resep.query.all()
        resep_data = [
            {
                'id': resep.id,
                'nama_resep': resep.nama_resep,
                'waktu_masak': resep.waktu_masak,
                'deskripsi_singkat': resep.deskripsi_singkat,
                'gambar': resep.gambar,
                'oleh': User.query.get(resep.dibuat_oleh).nama if resep.dibuat_oleh else 'Anonim'
            } for resep in resep_list
        ]
        # Render template dengan data resep
        return render_template('pages/home.html', resep_data=resep_data)
    except Exception as e:
        flash(f'Gagal memuat data resep: {str(e)}', 'danger')
        return render_template('pages/home.html', resep_data=[])