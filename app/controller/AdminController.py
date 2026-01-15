from app.model.resep import Resep
from app import app, response, db
from flask import request, session, render_template, redirect, url_for, flash

def topPick(id):
    """Menandai resep sebagai top pick"""
    if 'user_id' not in session or 'is_admin' not in session or not session['is_admin']:
        flash('Anda tidak memiliki izin untuk melakukan aksi ini', 'danger')
        return redirect(url_for('masuk'))
    
    try:
        resep = Resep.query.get_or_404(id)
        resep.is_top_pick = True
        db.session.commit()
        flash('Resep berhasil ditandai sebagai Top Pick!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menandai resep: {str(e)}', 'danger')
    
    return redirect(url_for('resep'))

def hapusPick(id):
    """Menghapus status top pick dari resep"""
    if 'user_id' not in session or 'is_admin' not in session or not session['is_admin']:
        flash('Anda tidak memiliki izin untuk melakukan aksi ini', 'danger')
        return redirect(url_for('masuk'))
    
    try:
        resep = Resep.query.get_or_404(id)
        resep.is_top_pick = False
        db.session.commit()
        flash('Status Top Pick berhasil dihapus!', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus status Top Pick: {str(e)}', 'danger')
    
    return redirect(url_for('resep'))

def set_top_pick(id):
    """API untuk menandai resep sebagai top pick"""
    return topPick(id)

def remove_top_pick(id):
    """API untuk menghapus status top pick"""
    return hapusPick(id)
