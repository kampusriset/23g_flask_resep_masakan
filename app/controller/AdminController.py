from app.model.resep import Resep
from app import app, response, db
from flask import request, session, render_template, redirect, url_for, flash

def topPick(id):
    if 'is_admin' not in session or not session['is_admin']:
        url_for('masuk')  # Hanya admin yang bisa mengakses
    
    resep = Resep.query.get_or_404(id)
    resep.is_top_pick = True  # Menandai resep sebagai Top Pick
    db.session.commit()  # Simpan perubahan ke database
    
    flash('Resep berhasil ditandai sebagai Top Pick!', 'success')
    return redirect(url_for('resep'))

def hapusPick(id):
    if 'is_admin' not in session or not session['is_admin']:
        url_for('masuk')  # Hanya admin yang bisa mengakses
    
    resep = Resep.query.get_or_404(id)
    resep.is_top_pick = False  # Menghapus status Top Pick
    db.session.commit()  # Simpan perubahan ke database
    
    flash('Status Top Pick berhasil dihapus!', 'info')
    return redirect(url_for('resep'))
