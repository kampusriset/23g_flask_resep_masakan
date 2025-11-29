from flask import session, redirect, url_for, flash
from app.model.user import User
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu untuk mengakses halaman ini.', 'danger')
            return redirect(url_for('masuk'))  # Ganti dengan nama fungsi view login Anda
        user = User.query.get(session['user_id'])  # Ambil user berdasarkan user_id di session
        if user.role != 'admin':
            flash('Akses ditolak! Anda bukan admin.', 'danger')
            return redirect(url_for('masuk'))  # Redirect ke halaman yang sesuai jika bukan admin
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu untuk mengakses halaman ini.', 'danger')
            return redirect(url_for('login'))  # Ganti dengan nama fungsi view login Anda
        user = User.query.get(session['user_id'])  # Ambil user berdasarkan user_id di session
        if user.role != 'user':
            flash('Akses ditolak! Anda bukan user.', 'danger')
            return redirect(url_for('login'))  # Redirect ke halaman yang sesuai jika bukan admin
        return f(*args, **kwargs)
    return decorated_function
