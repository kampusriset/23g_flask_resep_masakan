-- Cookify MySQL schema (phpMyAdmin import)
-- Engine: InnoDB, Charset: utf8mb4

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `favorit`;
DROP TABLE IF EXISTS `resep`;
DROP TABLE IF EXISTS `sorotan`;
DROP TABLE IF EXISTS `kategori`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nama` VARCHAR(250) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(250) NOT NULL,
  `role` VARCHAR(250) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kategori` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nama_kategori` VARCHAR(250) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `resep` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nama_resep` VARCHAR(250) NOT NULL,
  `gambar` VARCHAR(500) NOT NULL,
  `waktu_masak` INT NOT NULL,
  `kategori_id` BIGINT NOT NULL,
  `deskripsi_singkat` TEXT NOT NULL,
  `alat_dan_bahan` TEXT NOT NULL,
  `langkah_langkah` TEXT NOT NULL,
  `dibuat_oleh` BIGINT NOT NULL,
  `is_top_pick` TINYINT(1) DEFAULT 0,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  KEY `idx_resep_kategori` (`kategori_id`),
  KEY `idx_resep_pembuat` (`dibuat_oleh`),
  CONSTRAINT `fk_resep_kategori` FOREIGN KEY (`kategori_id`) REFERENCES `kategori` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_resep_user` FOREIGN KEY (`dibuat_oleh`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sorotan` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nama_sorotan` VARCHAR(250) NOT NULL,
  `gambar_sorotan` VARCHAR(500) NOT NULL,
  `waktu_sorotan` INT NOT NULL,
  `kategori_id` INT NOT NULL,
  `deskripsi_sorotan` TEXT NOT NULL,
  `alat_sorotan` TEXT NOT NULL,
  `langkah_sorotan` TEXT NOT NULL,
  `penulis` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  KEY `idx_sorotan_kategori` (`kategori_id`),
  KEY `idx_sorotan_penulis` (`penulis`),
  CONSTRAINT `fk_sorotan_kategori` FOREIGN KEY (`kategori_id`) REFERENCES `kategori` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_sorotan_user` FOREIGN KEY (`penulis`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `favorit` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `resep_id` BIGINT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  KEY `idx_favorit_user` (`user_id`),
  KEY `idx_favorit_resep` (`resep_id`),
  CONSTRAINT `fk_favorit_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_favorit_resep` FOREIGN KEY (`resep_id`) REFERENCES `resep` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS=1;
