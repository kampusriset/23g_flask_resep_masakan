from app import app, render_template, db
from flask import request, jsonify, session, send_file, flash, redirect, url_for
from app.controller import UserController, KategoriController, ResepController, SorotanController, ProfilController, FavoritController, AdminController
from app.decorators import admin_required, login_required
from app.model.user import User
from app.model.kategori import Kategori
from app.model.resep import Resep
from app.model.sorotan import Sorotan
from app.model.favorit import Favorit
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from io import BytesIO
from datetime import datetime
import re
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from app.model.resep import Resep


try:
    from openpyxl import Workbook
except ImportError:  # pragma: no cover - dependency hint
    Workbook = None

try:
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
except ImportError:  # pragma: no cover - dependency hint
    SimpleDocTemplate = None


@app.route('/')
def index():
    query = request.args.get('query', '').strip()  # Ambil parameter pencarian dari URL
    
    if query:  # Jika ada query, lakukan pencarian
        results = Resep.query.filter(
            Resep.nama_resep.ilike(f"%{query}%") |
            Resep.deskripsi_singkat.ilike(f"%{query}%") |
            Resep.alat_dan_bahan.ilike(f"%{query}%")
        ).all()
        return render_template('pages/pencarian.html', results=results, query=query)
    
    resep_data = Resep.query.options(joinedload(Resep.pembuat)).all()
    sorotan_data = Sorotan.query.options(joinedload(Sorotan.pembuat)).all()
    resep_top_pick = Resep.query.filter_by(is_top_pick=True).all()
    

    return render_template('pages/home.html', resep=resep_data, sorotan=sorotan_data, resep_top_pick=resep_top_pick)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return UserController.login()
    else:
        return render_template('pages/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return UserController.buatUser()
    else:
        return render_template('pages/register.html')

@app.route('/kategori')
def kategori():
    return ResepController.kategori()

@app.route('/resep')
def daftar_resep():
    from app.controller.ResepController import index
    return index()

@app.route('/details/<string:jenis>/<int:id>')
def details(jenis, id):
    return ResepController.details(jenis, id)

@app.route('/profil')
@login_required
def profil():
    reseps = Resep.query.filter_by(dibuat_oleh=session.get('user_id')).all()
    resep_list = Resep.query.all()
    kategoris = Kategori.query.all()
    favorit_list = Favorit.query.filter_by(user_id=session.get('user_id')).all()
    resep_favorit = [f.resep for f in favorit_list]
    return render_template('pages/profil.html', kategoris=kategoris, reseps=reseps, resep_list=resep_list, resep_favorit=resep_favorit)

@app.route('/profil/add', methods=['POST'])
def tambahResep():
    return ProfilController.tambahResep()

@app.route('/profil/update/<int:id>', methods=['POST'])
def editResep(id):
    return ProfilController.editResep(id)

@app.route('/profil/delete/<int:id>', methods=['POST'])
def hapusResep(id):
    return ProfilController.hapusResep(id)

@app.route('/tentang')
def kontak():
    return render_template('pages/tentang.html')

@app.route('/admin')
@admin_required  # Hanya admin yang bisa mengakses halaman ini
def admin():
    total_users = User.query.count()
    total_resep = Resep.query.count()
    total_kategori = Kategori.query.count()

    kategori_data = (
        db.session.query(
            Kategori.nama_kategori,
            func.count(Resep.id).label('jumlah')
        )
        .join(Resep, Kategori.id == Resep.kategori_id, isouter=True)
        .group_by(Kategori.id)
        .all()
    )

    chart_labels = [nama for nama, _ in kategori_data]
    chart_data = [jumlah for _, jumlah in kategori_data]
    chart_colors = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796']

    return render_template(
        'admin/index.html',
        total_users=total_users,
        total_resep=total_resep,
        total_kategori=total_kategori,
        chart_labels=chart_labels,
        chart_data=chart_data,
        chart_colors=chart_colors,
    )

# These routes are kept for backward compatibility
@app.route('/admin/topPick/<int:id>', methods=['POST'])
def admin_top_pick_legacy(id):
    return AdminController.topPick(id)

@app.route('/admin/hapusPick/<int:id>', methods=['POST'])
def admin_hapus_pick_legacy(id):
    return AdminController.hapusPick(id)

@app.route('/admin/pengguna')
def pengguna():
    users = User.query.all()
    return render_template('admin/pengguna.html', users=users)

@app.route('/admin/deleteUser/<int:user_id>', methods=['POST'])
def deleteUser(user_id):
    return UserController.deleteUser(user_id)

@app.route('/admin/sorotan', methods=['GET'])
def sorotan():
    sorotans = Sorotan.query.all()
    kategoris = Kategori.query.all()
    sorotan_exists = Sorotan.query.first()
    return render_template('admin/sorotan.html', sorotans=sorotans, kategoris=kategoris, sorotan_exists=sorotan_exists)

@app.route('/admin/sorotan/add', methods=['POST'])
def saveSorotan():
    return SorotanController.saveSorotan()

@app.route('/admin/sorotan/update/<int:id>', methods=['POST'])
def updateSorotan(id):
    return SorotanController.updateSorotan(id)

@app.route('/admin/sorotan/delete/<int:id>', methods=['POST'])
def deleteSorotan(id):
    return SorotanController.deleteSorotan(id)

@app.route('/admin/resep')
@admin_required
def resep():
    """Route untuk menampilkan daftar resep di admin"""
    from app.controller.ResepController import resep_admin
    return resep_admin()


def _format_resep_export_row(resep: Resep, truncate: int = 100):
    return {
        'nama': resep.nama_resep,
        'kategori': resep.kategori.nama_kategori if resep.kategori else '-',
        'waktu_masak': f"{resep.waktu_masak} menit" if resep.waktu_masak is not None else '-',
        'deskripsi': (resep.deskripsi_singkat or '')[:truncate],
        'alat_bahan': (resep.alat_dan_bahan or '')[:truncate],
        'langkah': (resep.langkah_langkah or '')[:truncate],
        'pembuat': resep.pembuat.nama if resep.pembuat else 'Anonim',
    }


def _fetch_recipe_export_data():
    reseps = (
        Resep.query.options(joinedload(Resep.kategori), joinedload(Resep.pembuat))
        .order_by(Resep.nama_resep.asc())
        .all()
    )

    return [_format_resep_export_row(resep) for resep in reseps]


def _fetch_single_recipe_export_data(resep_id: int):
    resep = (
        Resep.query.options(joinedload(Resep.kategori), joinedload(Resep.pembuat))
        .get_or_404(resep_id)
    )
    return _format_resep_export_row(resep, truncate=500)


def _sanitize_filename_component(text: str):
    safe = re.sub(r'[^A-Za-z0-9_-]+', '_', text.strip())
    return safe or 'resep'


def _export_recipes_excel(redirect_endpoint: str, redirect_kwargs=None, rows=None, filename_prefix='data_resep'):
    if Workbook is None:
        flash('Fitur export Excel membutuhkan paket openpyxl. Silakan instal dengan perintah "pip install openpyxl".', 'danger')
        return redirect(url_for(redirect_endpoint, **(redirect_kwargs or {})))

    data = rows if rows is not None else _fetch_recipe_export_data()
    if not data:
        flash('Tidak ada data resep untuk diekspor.', 'info')
        return redirect(url_for(redirect_endpoint, **(redirect_kwargs or {})))

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Data Resep'

    headers = ['No', 'Nama Resep', 'Kategori', 'Waktu Masak', 'Deskripsi', 'Alat & Bahan', 'Langkah Masak', 'Pembuat']
    sheet.append(headers)

    for idx, item in enumerate(data, start=1):
        sheet.append([
            idx,
            item['nama'],
            item['kategori'],
            item['waktu_masak'],
            item['deskripsi'],
            item['alat_bahan'],
            item['langkah'],
            item['pembuat'],
        ])

    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)

    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(
        stream,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


def _export_recipes_pdf(redirect_endpoint: str, redirect_kwargs=None, rows=None, filename_prefix='data_resep'):
    if SimpleDocTemplate is None:
        flash('Fitur export PDF membutuhkan paket reportlab. Silakan instal dengan perintah "pip install reportlab".', 'danger')
        return redirect(url_for(redirect_endpoint, **(redirect_kwargs or {})))

    data = rows if rows is not None else _fetch_recipe_export_data()
    if not data:
        flash('Tidak ada data resep untuk diekspor.', 'info')
        return redirect(url_for(redirect_endpoint, **(redirect_kwargs or {})))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    table_data = [['No', 'Nama Resep', 'Kategori', 'Waktu Masak', 'Deskripsi', 'Alat & Bahan', 'Langkah Masak', 'Pembuat']]
    for idx, item in enumerate(data, start=1):
        table_data.append([
            idx,
            item['nama'],
            item['kategori'],
            item['waktu_masak'],
            item['deskripsi'],
            item['alat_bahan'],
            item['langkah'],
            item['pembuat'],
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e3656')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    doc.build([table])
    buffer.seek(0)

    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@app.route('/admin/resep/export/excel')
@admin_required
def export_resep_excel():
    return _export_recipes_excel('resep')


@app.route('/admin/resep/export/pdf')
@admin_required
def export_resep_pdf():
    return _export_recipes_pdf('resep')


@app.route('/resep/export/excel')
def export_resep_excel_public():
    return _export_recipes_excel('daftar_resep')


@app.route('/resep/export/pdf')
def export_resep_pdf_public():
    return _export_recipes_pdf('daftar_resep')


@app.route('/resep/<int:resep_id>/export/excel')
def export_single_resep_excel(resep_id):
    row = _fetch_single_recipe_export_data(resep_id)
    prefix = f"resep_{_sanitize_filename_component(row['nama'])}"
    return _export_recipes_excel('details', redirect_kwargs={'jenis': 'resep', 'id': resep_id}, rows=[row], filename_prefix=prefix)


@app.route('/resep/<int:resep_id>/export/pdf')
def export_single_resep_pdf(resep_id):
    row = _fetch_single_recipe_export_data(resep_id)
    prefix = f"resep_{_sanitize_filename_component(row['nama'])}"
    return _export_recipes_pdf('details', redirect_kwargs={'jenis': 'resep', 'id': resep_id}, rows=[row], filename_prefix=prefix)

@app.route('/admin/resep/set-top-pick/<int:id>', methods=['POST'])
@admin_required
def set_resep_top_pick(id):
    from app.controller.AdminController import set_top_pick
    return set_top_pick(id)

# Route untuk menghapus top pick dari resep
@app.route('/admin/resep/remove-top-pick/<int:id>', methods=['POST'])
@admin_required
def remove_resep_top_pick(id):
    from app.controller.AdminController import remove_top_pick
    return remove_top_pick(id)

@app.route('/admin/resep/save', methods=['POST'])
@admin_required
def saveResep():
    from app.controller.ResepController import saveResep
    return saveResep()

@app.route('/admin/resep/update/<int:id>', methods=['POST'])
@admin_required
def updateResep(id):
    from app.controller.ResepController import updateResep
    return updateResep(id)

@app.route('/admin/resep/delete/<int:id>', methods=['POST'])
@admin_required
def deleteResep(id):
    from app.controller.ResepController import deleteResep
    return deleteResep(id)

@app.route('/admin/category', methods=['GET'])
def category():
    kategoris = Kategori.query.all()
    return render_template('admin/kategori.html', kategoris=kategoris)

@app.route('/admin/category/add', methods=['POST'])
def saveKategori():
    return KategoriController.saveKategori()

@app.route('/admin/category/update/<int:id>', methods=['POST'])
def updateKategori(id):
    return KategoriController.updateKategori(id)

@app.route('/admin/category/delete/<int:id>', methods=['POST'])
def deleteKategori(id):
    return KategoriController.deleteKategori(id)


@app.route('/admin/daftar', methods=['GET','POST'])
def daftar():
    if request.method == 'POST':
        return UserController.buatAdmin()
    else:
        return render_template('admin/daftar.html')

@app.route('/admin/masuk', methods=['GET','POST'])
def masuk():
    if request.method == 'POST':
        return UserController.masuk()
    else:
        return render_template('admin/masuk.html')
    
@app.route('/logout')
def logout():
    return UserController.logout()

@app.route('/keluar')
def keluar():
    return UserController.keluar()

@app.route('/resep/favorit/<int:resep_id>', methods=['POST'])
def tambahFavorit(resep_id):
    return FavoritController.tambahFavorit(resep_id)

@app.route('/favorit/hapus/<int:resep_id>', methods=['POST'])
def hapusFavorit(resep_id):
    return FavoritController.hapusFavorit(resep_id)