-- ===========================================
-- LifeLink Blood Donation Management System
-- Database Schema
-- ===========================================

CREATE DATABASE IF NOT EXISTS louange_db;
USE louange_db;

-- ===========================================
-- Administrators
-- ===========================================

CREATE TABLE IF NOT EXISTS  administrators (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- Donors
-- ===========================================

CREATE TABLE IF NOT EXISTS donors (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    date_of_birth DATE NOT NULL,

    blood_type ENUM(
        'A+','A-',
        'B+','B-',
        'AB+','AB-',
        'O+','O-'
    ) NOT NULL,

    phone VARCHAR(20) NOT NULL,

    email VARCHAR(100) UNIQUE,

    district VARCHAR(100) NOT NULL,

    last_donation_date DATE DEFAULT NULL,

    is_available BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- Donation Locations
-- ===========================================

CREATE TABLE IF NOT EXISTS donation_locations (

    location_id INT AUTO_INCREMENT PRIMARY KEY,

    location_name VARCHAR(100) NOT NULL,

    district VARCHAR(100) NOT NULL
);

-- ===========================================
-- Donations
-- ===========================================

CREATE TABLE IF NOT EXISTS donations (

    donation_id INT AUTO_INCREMENT PRIMARY KEY,

    donor_id INT NOT NULL,

    location_id INT NOT NULL,

    donation_date DATE NOT NULL,

    volume_ml INT NOT NULL DEFAULT 450,

    FOREIGN KEY (donor_id)
        REFERENCES donors(donor_id)
        ON DELETE CASCADE,

    FOREIGN KEY (location_id)
        REFERENCES donation_locations(location_id)
        ON DELETE RESTRICT
);
