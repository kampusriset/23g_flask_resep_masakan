from app import app, render_template
from flask import request, jsonify, session
from app.controller import UserController, KategoriController, ResepController, SorotanController, ProfilController, FavoritController, AdminController
from app.decorators import admin_required, login_required
from app.model.user import User
from app.model.kategori import Kategori
from app.model.resep import Resep
from app.model.sorotan import Sorotan
from app.model.favorit import Favorit
from sqlalchemy.orm import joinedload


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
    total_reseps = Resep.query.count()
    return render_template('admin/index.html', total_users=total_users, total_reseps=total_reseps) 

@app.route('/admin/topPick/<int:id>', methods=['POST'])
def topPick(id):
    return AdminController.topPick(id)

@app.route('/admin/hapusPick/<int:id>', methods=['POST'])
def hapusPick(id):
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

@app.route('/admin/resep', methods=['GET'])
def resep():
    reseps = Resep.query.all()
    kategoris = Kategori.query.all()
    return render_template('admin/resep.html', reseps=reseps, kategoris=kategoris)

@app.route('/admin/resep/add', methods=['POST'])
def saveResep():
    return ResepController.saveResep()

@app.route('/admin/resep/update/<int:id>', methods=['POST'])
def updateResep(id):
    return ResepController.updateResep(id)

@app.route('/admin/resep/delete/<int:id>', methods=['POST'])
def deleteResep(id):
    return ResepController.deleteResep(id)

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




