-- =====================================================================
-- LifeLink Blood Donation Management System
-- Database schema (MySQL / MariaDB, InnoDB)
--
-- Owner: Gatete Irene (Database & Donations)
--
-- Conventions used (see Development Guide, sections 5 & 6):
--   * Each table's primary key is named <entity>_id (donor_id,
--     donation_id, ...). NOTE: the guide's literal wording is "primary
--     keys shall use id". We use <entity>_id because the already-merged
--     donor and search modules query `donor_id` directly. This is
--     flagged for the team to confirm as the standing convention.
--   * Foreign keys follow <referenced_table_singular>_id.
--   * All dates are stored as DATE in YYYY-MM-DD form.
--   * Passwords are NEVER stored in plain text (administrators holds a
--     one-way password_hash only).
--   * ENGINE=InnoDB on every table so FOREIGN KEY constraints are
--     actually enforced (MyISAM silently ignores them).
--
-- Safe to run repeatedly: uses CREATE ... IF NOT EXISTS.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS lifelink
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE lifelink;


-- ---------------------------------------------------------------------
-- donors
-- Owned data: Donor Information (Member 3). Table created by Member 4.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donors (
    donor_id            INT AUTO_INCREMENT PRIMARY KEY,
    full_name           VARCHAR(100) NOT NULL,
    blood_type          ENUM('A+', 'A-', 'B+', 'B-',
                             'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    district            VARCHAR(50)  NOT NULL,
    phone               VARCHAR(20)  NOT NULL,
    email               VARCHAR(100) DEFAULT NULL,
    date_of_birth       DATE         NOT NULL,
    last_donation_date  DATE         DEFAULT NULL,
    is_available        BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_donors_blood_type (blood_type),
    INDEX idx_donors_district   (district)
) ENGINE=InnoDB;


-- ---------------------------------------------------------------------
-- donation_locations
-- Owned data: Donation Locations (Member 5). Table created by Member 4.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donation_locations (
    location_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    district      VARCHAR(50)  DEFAULT NULL,
    address       VARCHAR(200) DEFAULT NULL,
    created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_locations_district (district)
) ENGINE=InnoDB;


-- ---------------------------------------------------------------------
-- administrators
-- Owned data: Administrator Information (Member 2). Table by Member 4.
-- password_hash stores a one-way hash only. NEVER a plain password.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS administrators (
    admin_id       INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(50)  NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    full_name      VARCHAR(100) DEFAULT NULL,
    created_at     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- ---------------------------------------------------------------------
-- donations
-- Owned data: Donation Records (Member 4).
-- Foreign keys:
--   donor_id    -> donors(donor_id)                [required]
--   location_id -> donation_locations(location_id) [optional]
-- A donor with existing donations cannot be deleted (RESTRICT), which
-- preserves donation history. Location deletion nulls the reference.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donations (
    donation_id    INT AUTO_INCREMENT PRIMARY KEY,
    donor_id       INT       NOT NULL,
    location_id    INT       DEFAULT NULL,
    donation_date  DATE      NOT NULL,
    volume_ml      INT       NOT NULL DEFAULT 450,
    notes          VARCHAR(255) DEFAULT NULL,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_donation_donor
        FOREIGN KEY (donor_id)
        REFERENCES donors (donor_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_donation_location
        FOREIGN KEY (location_id)
        REFERENCES donation_locations (location_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_donations_donor (donor_id),
    INDEX idx_donations_date  (donation_date)
) ENGINE=InnoDB;
