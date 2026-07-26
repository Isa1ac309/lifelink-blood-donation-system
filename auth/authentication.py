"""
Authentication Module
LifeLink Blood Donation Management System

Handles administrator registration and login.
"""

import bcrypt
import mysql.connector

from database.connection import get_db_connection


# ===========================================
# Password Utilities
# ===========================================

def hash_password(password: str) -> str:
    """
    Converts a plain-text password into a secure hash.
    """

    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies that a password matches its hash.
    """

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ===========================================
# Admin Functions
# ===========================================

def admin_exists(username: str) -> bool:

    connection = get_db_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    query = """
    SELECT admin_id
    FROM administrators
    WHERE username = %s
    """

    cursor.execute(query, (username,))

    exists = cursor.fetchone() is not None

    cursor.close()
    connection.close()

    return exists


def register_admin(username: str, password: str) -> dict:

    if admin_exists(username):

        return {
            "success": False,
            "message": "Username already exists."
        }

    hashed = hash_password(password)

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO administrators
    (username, password_hash)

    VALUES (%s,%s)
    """

    cursor.execute(
        query,
        (
            username,
            hashed
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "message": "Administrator created successfully."
    }


def login(username: str, password: str) -> dict:

    connection = get_db_connection()

    if not connection:

        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM administrators
    WHERE username=%s
    """

    cursor.execute(query, (username,))

    admin = cursor.fetchone()

    cursor.close()
    connection.close()

    if admin is None:

        return {
            "success": False,
            "message": "Administrator not found."
        }

    if verify_password(
        password,
        admin["password_hash"]
    ):

        return {
            "success": True,
            "message": "Login successful.",
            "admin": admin
        }

    return {
        "success": False,
        "message": "Incorrect password."
    }


# ===========================================
# Testing
# ===========================================

if __name__ == "__main__":

    print(register_admin(
        "admin",
        "admin123"
    ))

    print(login(
        "admin",
        "admin123"
    ))