BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('8967aa432ec4');
CREATE TABLE favorit (
	id BIGINT NOT NULL, 
	user_id BIGINT NOT NULL, 
	resep_id BIGINT NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(resep_id) REFERENCES resep (id)
);
CREATE TABLE kategori (
	id INTEGER NOT NULL, 
	nama_kategori VARCHAR(250) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "kategori" VALUES(1,'Korean Food','2025-12-25 11:57:18.392460','2025-12-25 11:57:18.392467');
CREATE TABLE resep (
	id BIGINT NOT NULL, 
	nama_resep VARCHAR(250) NOT NULL, 
	gambar VARCHAR(500) NOT NULL, 
	waktu_masak INTEGER NOT NULL, 
	kategori_id BIGINT NOT NULL, 
	deskripsi_singkat TEXT NOT NULL, 
	alat_dan_bahan TEXT NOT NULL, 
	langkah_langkah TEXT NOT NULL, 
	dibuat_oleh BIGINT NOT NULL, 
	is_top_pick BOOLEAN, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(kategori_id) REFERENCES kategori (id), 
	FOREIGN KEY(dibuat_oleh) REFERENCES user (id)
);
CREATE TABLE sorotan (
	id INTEGER NOT NULL, 
	nama_sorotan VARCHAR(250) NOT NULL, 
	gambar_sorotan VARCHAR(500) NOT NULL, 
	waktu_sorotan INTEGER NOT NULL, 
	kategori_id INTEGER NOT NULL, 
	deskripsi_sorotan TEXT NOT NULL, 
	alat_sorotan TEXT NOT NULL, 
	langkah_sorotan TEXT NOT NULL, 
	penulis INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(kategori_id) REFERENCES kategori (id), 
	FOREIGN KEY(penulis) REFERENCES user (id)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	nama VARCHAR(250) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	password VARCHAR(250) NOT NULL, 
	role VARCHAR(250) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO "user" VALUES(1,'Admin','admin@example.com','admin123','admin','2025-12-25 11:57:18.404229','2025-12-25 11:57:18.404237');
COMMIT;
