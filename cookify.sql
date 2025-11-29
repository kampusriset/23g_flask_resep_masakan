/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

REPLACE INTO `alembic_version` (`version_num`) VALUES
	('8967aa432ec4');

CREATE TABLE IF NOT EXISTS `favorit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `resep_id` bigint NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `resep_id` (`resep_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `favorit_ibfk_1` FOREIGN KEY (`resep_id`) REFERENCES `resep` (`id`),
  CONSTRAINT `favorit_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `kategori` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(250) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

REPLACE INTO `kategori` (`id`, `nama_kategori`, `created_at`, `updated_at`) VALUES
	(1, 'kangen masakan nenek', '2025-11-28 21:28:54', '2025-11-28 15:58:01');

CREATE TABLE IF NOT EXISTS `resep` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama_resep` varchar(250) NOT NULL,
  `gambar` varchar(500) NOT NULL,
  `waktu_masak` int NOT NULL,
  `kategori_id` bigint NOT NULL,
  `deskripsi_singkat` text NOT NULL,
  `alat_dan_bahan` text NOT NULL,
  `langkah_langkah` text NOT NULL,
  `dibuat_oleh` bigint NOT NULL,
  `is_top_pick` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dibuat_oleh` (`dibuat_oleh`),
  KEY `kategori_id` (`kategori_id`),
  CONSTRAINT `resep_ibfk_1` FOREIGN KEY (`dibuat_oleh`) REFERENCES `user` (`id`),
  CONSTRAINT `resep_ibfk_2` FOREIGN KEY (`kategori_id`) REFERENCES `kategori` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

REPLACE INTO `resep` (`id`, `nama_resep`, `gambar`, `waktu_masak`, `kategori_id`, `deskripsi_singkat`, `alat_dan_bahan`, `langkah_langkah`, `dibuat_oleh`, `is_top_pick`, `created_at`, `updated_at`) VALUES
	(2, 'jamur kecubung', 'app/static/uploads/167-1672254_logo-halal-png.png', 1, 1, 'maboookkk doloooo!!', 'kecubung\r\njamurr lethooong', 'makan mentah mentah!!!', 1, 0, '2025-11-28 15:21:28', '2025-11-28 15:21:28');

CREATE TABLE IF NOT EXISTS `sorotan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama_sorotan` varchar(250) NOT NULL,
  `gambar_sorotan` varchar(500) NOT NULL,
  `waktu_sorotan` int NOT NULL,
  `kategori_id` bigint NOT NULL,
  `deskripsi_sorotan` text NOT NULL,
  `alat_sorotan` text NOT NULL,
  `langkah_sorotan` text NOT NULL,
  `penulis` bigint NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `kategori_id` (`kategori_id`),
  KEY `penulis` (`penulis`),
  CONSTRAINT `sorotan_ibfk_1` FOREIGN KEY (`kategori_id`) REFERENCES `kategori` (`id`),
  CONSTRAINT `sorotan_ibfk_2` FOREIGN KEY (`penulis`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

REPLACE INTO `sorotan` (`id`, `nama_sorotan`, `gambar_sorotan`, `waktu_sorotan`, `kategori_id`, `deskripsi_sorotan`, `alat_sorotan`, `langkah_sorotan`, `penulis`, `created_at`, `updated_at`) VALUES
	(1, 'anjay', 'app/static/uploads/gambar_logo_amikom.jpg', 2, 1, 'opo iki', 'byuuuh', 'eaaaakkkk', 2, '2025-11-28 16:01:58', '2025-11-28 16:01:58');

CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama` varchar(250) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(250) NOT NULL,
  `role` varchar(250) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

REPLACE INTO `user` (`id`, `nama`, `email`, `password`, `role`, `created_at`, `updated_at`) VALUES
	(1, 'user', 'user@gmail.com', 'pbkdf2:sha256:1000000$RbtBEVnyRGTiiGSs$9a27cbf98ba0b25ec07c04439fbc8cd5554ca4ea5e2c865aaeb880c7c0f4a820', 'user', '2025-11-28 14:26:19', '2025-11-28 14:26:19'),
	(2, 'admin', 'admin@gmail.com', 'pbkdf2:sha256:1000000$RbtBEVnyRGTiiGSs$9a27cbf98ba0b25ec07c04439fbc8cd5554ca4ea5e2c865aaeb880c7c0f4a820', 'admin', '2025-11-28 23:00:42', '2025-11-28 23:00:42');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
