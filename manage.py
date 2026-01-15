import os
from app import app, db
from app.model import user, kategori, resep, sorotan, favorit
from datetime import datetime
import click
from flask.cli import with_appcontext

@app.cli.group()
def db_commands():
    """Database management commands."""
    pass

@db_commands.command('init')
@with_appcontext
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Database initialized successfully!')

@db_commands.command('drop')
@with_appcontext
def drop_db():
    """Drop all database tables."""
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        click.echo('All tables dropped!')

@db_commands.command('reset')
@with_appcontext
def reset_db():
    """Drop and recreate all database tables."""
    if click.confirm('Are you sure you want to reset the database? This will delete all data!'):
        db.drop_all()
        db.create_all()
        click.echo('Database reset complete!')

def seed_sample_data():
    """Seed the database with sample data."""
    from app.model.user import User
    from app.model.kategori import Kategori
    from app.model.resep import Resep
    
    # Add sample categories
    categories = [
        Kategori(nama_kategori='Makanan Utama'),
        Kategori(nama_kategori='Makanan Pembuka'),
        Kategori(nama_kategori='Makanan Penutup'),
        Kategori(nama_kategori='Minuman'),
        Kategori(nama_kategori='Kue')
    ]
    
    for category in categories:
        db.session.add(category)
    
    # Add a sample user
    user = User(
        nama='Admin User',
        email='admin@example.com',
        role='admin'
    )
    # Hash password via model method for compatibility with login() check
    user.setPassword('admin123')
    db.session.add(user)
    
    db.session.commit()
    
    # Add a sample recipe
    recipe = Resep(
        nama_resep='Nasi Goreng Spesial',
        gambar='nasi-goreng.jpg',
        waktu_masak=30,
        kategori_id=1,  # Makanan Utama
        deskripsi_singkat='Nasi goreng spesial dengan bumbu rahasia',
        alat_dan_bahan='- Nasi 2 piring\n- Bawang putih 3 siung\n- Kecap asin 2 sdm\n- Telur 2 butir\n- Ayam suwir secukupnya',
        langkah_langkah='1. Tumis bawang putih hingga harum\n2. Masukkan telur, orak-arik\n3. Tambahkan nasi dan bumbu\n4. Aduk rata dan sajikan',
        dibuat_oleh=1,
        is_top_pick=True
    )
    db.session.add(recipe)
    
    db.session.commit()
    click.echo('Sample data added successfully!')

@db_commands.command('seed')
@with_appcontext
def seed_db():
    """Seed the database with sample data."""
    seed_sample_data()

if __name__ == '__main__':
    import sys
    # Jalankan perintah langsung tanpa Flask CLI, cocok untuk PowerShell
    with app.app_context():
        if len(sys.argv) < 2:
            print('Usage: python manage.py [init|drop|reset|seed]')
            sys.exit(1)

        cmd = sys.argv[1].lower()
        if cmd == 'init':
            db.create_all()
            print('Database initialized successfully!')
        elif cmd == 'drop':
            db.drop_all()
            print('All tables dropped!')
        elif cmd == 'reset':
            db.drop_all()
            db.create_all()
            print('Database reset complete!')
        elif cmd == 'seed':
            seed_sample_data()
        else:
            print(f'Unknown command: {cmd}')
            print('Usage: python manage.py [init|drop|reset|seed]')
