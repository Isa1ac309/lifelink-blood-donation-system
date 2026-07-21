"""
auth/authentication.py

Authentication module for the LifeLink Blood Donation Management System.

Day 1 scope: function stubs and docstrings only. Full implementation
(password hashing with bcrypt, session handling, etc.) begins Day 2.
"""

import bcrypt


def register_admin(full_name, email, phone, password):
    """
    Register a new admin/staff account.

    Args:
        full_name (str): Full name of the admin.
        email (str): Admin's email address, used for login.
        phone (str): Admin's phone number, used for login.
        password (str): Plaintext password to be hashed and stored.

    Returns:
        dict: The newly created admin record (without the plaintext
            password), or an error message if registration fails
            (e.g. missing fields or duplicate email/phone).

    Day 2 TODO:
        - Validate required fields are present.
        - Check for duplicate email/phone in the database.
        - Hash the password using hash_password() before storing.
        - Insert the new admin record into the database.
    """
    pass


def login(identifier, password):
    """
    Authenticate a user (admin or donor) using their email or phone
    number plus password, and start a session on success.

    Args:
        identifier (str): The user's email address or phone number.
        password (str): The plaintext password supplied at login.

    Returns:
        dict: Session/user info on successful authentication, or
            an error message on failure (invalid credentials).

    Day 2 TODO:
        - Look up the user record by email or phone.
        - Verify the password using verify_password().
        - Create a session with an expiry for auto-logout after
          15-30 minutes of inactivity (per the non-functional
          security requirement).
    """
    pass


def logout(session_id):
    """
    End an active user session.

    Args:
        session_id (str): Identifier of the session to terminate.

    Returns:
        bool: True if the session was successfully ended, False
            if no matching session was found.

    Day 2 TODO:
        - Invalidate/remove the session from session storage.
        - Handle the case where the session has already expired.
    """
    pass


def hash_password(plain_password):
    """
    Hash a plaintext password using bcrypt so it is never stored
    in plain text, per the system's security requirements.

    Args:
        plain_password (str): The plaintext password to hash.

    Returns:
        str: The bcrypt password hash.

    Day 2 TODO:
        - Implement using bcrypt.hashpw() with a generated salt.
    """
    pass


def verify_password(plain_password, hashed_password):
    """
    Verify a plaintext password against a previously stored bcrypt hash.

    Args:
        plain_password (str): The plaintext password supplied at login.
        hashed_password (str): The bcrypt hash stored for this user.

    Returns:
        bool: True if the password matches the hash, False otherwise.

    Day 2 TODO:
        - Implement using bcrypt.checkpw().
    """
    pass


if