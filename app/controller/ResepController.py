import os
from werkzeug.utils import secure_filename
from app.model.resep import Resep
from app.model.kategori import Kategori
from app.model.user import User
from app.model.sorotan import Sorotan
from app import app, response, db
from flask import request, jsonify, session, render_template, redirect, url_for, flash
from functools import wraps

# Path untuk menyimpan gambar
UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])  # Membuat folder jika belum ada

def saveResep():
    try:
        nama_resep = request.form.get('nama_resep')
        waktu_masak = request.form.get('waktu_masak')
        deskripsi_singkat = request.form.get('deskripsi_singkat')
        alat_dan_bahan = request.form.get('alat_dan_bahan')
        langkah_langkah = request.form.get('langkah_langkah')
        kategori_id = int(request.form.get('kategori_id'))
        
        print(f"nama_resep: {nama_resep}, waktu_masak: {waktu_masak}, deskripsi_singkat: {deskripsi_singkat}, alat_dan_bahan: {alat_dan_bahan}, langkah_langkah: {langkah_langkah}, kategori_id: {kategori_id}, gambar: {request.files.get('gambar')}, dibuat_oleh: {session.get('user_id')}")
        
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
    return redirect(url_for('resep'))


def updateResep(id):
    resep = Resep.query.get_or_404(id)
    try:
        # Perbarui data dari form
        resep.nama_resep = request.form.get('nama_resep')
        resep.waktu_masak = request.form.get('waktu_masak')
        resep.deskripsi_singkat = request.form.get('deskripsi_singkat')
        resep.alat_dan_bahan = request.form.get('alat_dan_bahan')
        resep.langkah_langkah = request.form.get('langkah_langkah')
        resep.kategori_id = int(request.form.get('kategori_id'))

        # Update gambar jika ada file baru
        file = request.files.get('gambar')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
            file.save(filepath)
            resep.gambar = filepath

        db.session.commit()
        flash('Resep berhasil diperbarui!', 'success')
    except Exception as e:
        flash(f'Gagal memperbarui resep: {str(e)}', 'danger')
    return redirect(url_for('resep'))


def deleteResep(id):
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
    return redirect(url_for('resep'))

# Menampilkan resep rekomendasi
def index():
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
    
# Menampilkan resep kategori
def kategori():
    kategori_list = Kategori.query.all()

    # Ambil semua resep, tetapi jika kategori dipilih, filter berdasarkan kategori tersebut
    kategori_id = request.args.get('kategori_id', None)

    if kategori_id:
        # Filter resep berdasarkan kategori yang dipilih
        resep_query = Resep.query.filter_by(kategori_id=kategori_id).all()
    else:
        # Ambil semua resep jika tidak ada kategori yang dipilih
        resep_query = Resep.query.all()

    # Tambahkan informasi pembuat (oleh) ke dalam daftar resep
    resep_list = []
    for resep in resep_query:
        pembuat = User.query.get(resep.dibuat_oleh)  # Ambil user berdasarkan ID
        resep_data = {
            'id': resep.id,
            'nama_resep': resep.nama_resep,
            'gambar': resep.gambar,
            'waktu_masak': resep.waktu_masak,
            'kategori_id': resep.kategori_id,
            'deskripsi_singkat': resep.deskripsi_singkat,
            'alat_dan_bahan': resep.alat_dan_bahan,
            'langkah_langkah': resep.langkah_langkah,
            'dibuat_oleh': resep.dibuat_oleh,
            'oleh': pembuat.nama if pembuat else 'Anonim',  # Tambahkan nama pembuat
        }
        resep_list.append(resep_data)

    return render_template('pages/kategori.html', kategori_list=kategori_list, resep_list=resep_list)


def details(jenis, id):
    try:
        if 'user_id' not in session:  # Misalnya user_id disimpan di session setelah login
            flash('Silakan login untuk mengakses halaman ini', 'warning')
            return redirect(url_for('login'))
        # Cek jenis data (resep atau sorotan)
        if jenis == 'resep':
            data = Resep.query.get_or_404(id)
            result = {
                "id": data.id,
                "nama": data.nama_resep,
                "gambar": data.gambar,
                "waktu": data.waktu_masak,
                "deskripsi": data.deskripsi_singkat,
                "alat_dan_bahan": data.alat_dan_bahan.split("\n"),  # Asumsikan alat dan bahan disimpan sebagai teks dipisahkan baris
                "langkah_langkah": data.langkah_langkah.split("\n"),  # Asumsikan langkah disimpan sebagai teks dipisahkan baris
                "oleh": data.pembuat.nama if data.pembuat else "Anonim",
                "kategori": data.kategori.nama_kategori
            }
        elif jenis == 'sorotan':
            data = Sorotan.query.get_or_404(id)
            result = {
                "id": data.id,
                "nama": data.nama_sorotan,
                "gambar": data.gambar_sorotan,
                "waktu": data.waktu_sorotan,
                "deskripsi": data.deskripsi_sorotan,
                "alat_dan_bahan": data.alat_sorotan.split("\n"),  # Asumsikan alat dan bahan disimpan sebagai teks dipisahkan baris
                "langkah_langkah": data.langkah_sorotan.split("\n"),  # Asumsikan langkah disimpan sebagai teks dipisahkan baris
                "oleh": data.pembuat.nama if data.pembuat else "Anonim",
                "kategori": data.kategori.nama_kategori
            }
        else:
            flash("Jenis data tidak valid.", "danger")
            return redirect(url_for('index'))  # Alihkan ke halaman utama atau kategori

        # Render template dengan data
        return render_template('pages/details.html', data=result, jenis=jenis)

    except Exception as e:
        flash(f"Gagal memuat data: {str(e)}", "danger")
        return redirect(url_for('index'))
    

def resep_admin():
    """Menampilkan daftar resep di halaman admin"""
    try:
        # Ambil semua resep beserta relasinya
        reseps = Resep.query.options(
            db.joinedload(Resep.kategori),
            db.joinedload(Resep.pembuat)
        ).all()
        
        # Ambil daftar kategori untuk form filter/tambah
        kategoris = Kategori.query.all()
        
        return render_template(
            'admin/resep.html',
            reseps=reseps,
            kategoris=kategoris
        )
    except Exception as e:
        flash(f'Gagal memuat data resep: {str(e)}', 'danger')
        return redirect(url_for('admin'))