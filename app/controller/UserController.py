from app.model.user import User
from app import app, response, db
from flask import request, jsonify, session, render_template, redirect, url_for, flash

def buatAdmin():
    try:
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        role = "admin"
        users = User(nama=nama, email=email, role=role)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        

        # Redirect ke halaman login admin
        flash('Admin berhasil dibuat!', 'success')
        return redirect(url_for('masuk'))  # Arahkan ke halaman login admin

    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return redirect(url_for('daftar'))
    
# def singleObject(data):
#     data = {
#         'id' : data.id,
#         'username' : data.username,
#         'email' : data.email,
#         'role' : data.role
#     }
    
#     return data   
def masuk():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.checkPassword(password):
            if user.role == 'admin':  # Cek apakah pengguna adalah admin
                session['user_id'] = user.id  # Simpan id user ke session
                flash('Login berhasil!', 'success')
                return redirect(url_for('admin'))  # Redirect ke halaman dashboard admin
            else:
                flash('Akses ditolak! Anda bukan admin.', 'danger')
                return redirect(url_for('masuk'))
        else:
            flash('Email atau password salah!', 'danger')
            return redirect(url_for('masuk'))

def buatUser():
    try:
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        role = "user"
        
        users = User(nama=nama, email=email, role=role)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        
        flash('Registrasi berhasil!', 'success')
        return redirect(url_for('login'))  # Arahkan ke halaman login pengguna

    except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('register'))  # Jika ada kesalahan, kembali ke form
        
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email dan password harus diisi!', 'error')
            return render_template('pages/login.html')
            
        user = User.query.filter_by(email=email).first()

        if user and user.checkPassword(password):
            if user.role == 'user':
                session['user_id'] = user.id
                session['is_admin'] = False
                flash('Login berhasil!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Akses ditolak! Gunakan halaman admin untuk login.', 'error')
        else:
            flash('Email atau password salah!', 'error')
    
    return render_template('pages/login.html')
        
def logout():
    session.pop('user_id', None)
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('index'))

def keluar():
    session.pop('user_id', None)
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('masuk'))

def deleteUser(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('Pengguna berhasil dihapus.', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan saat menghapus pengguna: {str(e)}', 'danger')
    return redirect(url_for('pengguna'))
