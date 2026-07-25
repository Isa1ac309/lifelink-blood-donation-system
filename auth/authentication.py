"""
auth/authentication.py

Authentication module for the LifeLink Blood Donation Management System.

Day 2: real implementation of admin registration, login, logout,
password hashing/verification, and simple in-memory session management.

Expected admins table (MySQL):
    CREATE TABLE admins (
        admin_id      INT AUTO_INCREMENT PRIMARY KEY,
        full_name     VARCHAR(100) NOT NULL,
        email         VARCHAR(100) UNIQUE,
        phone         VARCHAR(20) UNIQUE,
        password_hash VARCHAR(255) NOT NULL
    );

If Member 4's shared database.connection module isn't ready yet, this
file falls back to its own local get_connection() so it still runs —
swap DB_CONFIG below for the team's real shared connection once available.
"""

import time
import uuid
import bcrypt
import mysql.connector
from mysql.connector import Error

# --- Database connection -----------------------------------------------
# TODO (integration): replace this with the team's shared
# database.connection.get_connection() once Member 4's module is ready.
import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "mysql-6159335-alustudent-6978.k.aivencloud.com"),
    "port": int(os.environ.get("DB_PORT", 21312)),
    "user": os.environ.get("DB_USER", "avnadmin"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME", "defaultdb"),
}


def get_connection():
    """Open and return a new MySQL connection using DB_CONFIG."""
    return mysql.connector.connect(**DB_CONFIG)


# --- Session management (simple in-memory store) ------------------------
# session_id -> {"identifier": str, "expires_at": float}
_SESSIONS = {}
SESSION_TIMEOUT_SECONDS = 20 * 60  # 20 minutes, within the 15-30 min spec


def _create_session(identifier):
    """Create a new session for a logged-in user and return its id."""
    session_id = str(uuid.uuid4())
    _SESSIONS[session_id] = {
        "identifier": identifier,
        "expires_at": time.time() + SESSION_TIMEOUT_SECONDS,
    }
    return session_id


def _touch_session(session_id):
    """Refresh a session's expiry (call this on each authenticated action)."""
    if session_id in _SESSIONS:
        _SESSIONS[session_id]["expires_at"] = time.time() + SESSION_TIMEOUT_SECONDS


def is_session_valid(session_id):
    """Return True if the session exists and hasn't expired."""
    session = _SESSIONS.get(session_id)
    if session is None:
        return False
    if time.time() > session["expires_at"]:
        del _SESSIONS[session_id]
        return False
    return True


# --- Password hashing -----------------------------------------------------

def hash_password(plain_password):
    """Hash a plaintext password with bcrypt and return it as a string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password, hashed_password):
    """Return True if plain_password matches the stored bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# --- Input validation -----------------------------------------------------

def _validate_login_input(identifier, password):
    """Return an error message string, or None if input is valid."""
    if not identifier or not identifier.strip():
        return "Email or phone number is required."
    if not password:
        return "Password is required."
    return None


# --- Core authentication functions ----------------------------------------

def register_admin(full_name, email, phone, password):
    """
    Register a new admin account with a securely hashed password.

    Returns:
        dict: {"success": True, "admin_id": <id>} on success, or
              {"success": False, "error": <message>} on failure.
    """
    if not full_name or not email or not phone or not password:
        return {"success": False, "error": "All fields are required."}

    password_hash = hash_password(password)

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO admins (full_name, email, phone, password_hash) "
            "VALUES (%s, %s, %s, %s)",
            (full_name, email, phone, password_hash),
        )
        connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return {"success": True, "admin_id": new_id}
    except Error as e:
        # Covers duplicate email/phone (unique constraint) and other DB errors
        return {"success": False, "error": str(e)}


def login(identifier, password):
    """
    Authenticate an admin by email or phone plus password, and start
    a session on success.

    Returns:
        dict: {"success": True, "session_id": <id>, "admin_id": <id>}
              on success, or {"success": False, "error": <message>}.
    """
    validation_error = _validate_login_input(identifier, password)
    if validation_error:
        return {"success": False, "error": validation_error}

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT admin_id, password_hash FROM admins "
            "WHERE email = %s OR phone = %s",
            (identifier, identifier),
        )
        admin = cursor.fetchone()
        cursor.close()
        connection.close()
    except Error as e:
        return {"success": False, "error": str(e)}

    if admin is None:
        return {"success": False, "error": "Invalid credentials."}

    if not verify_password(password, admin["password_hash"]):
        return {"success": False, "error": "Invalid credentials."}

    session_id = _create_session(identifier)
    return {"success": True, "session_id": session_id, "admin_id": admin["admin_id"]}


def logout(session_id):
    """
    End an active session.

    Returns:
        bool: True if a session was found and ended, False otherwise.
    """
    if session_id in _SESSIONS:
        del _SESSIONS[session_id]
        return True
    return False