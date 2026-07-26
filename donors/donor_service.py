"""
Donor Management Service
LifeLink Blood Donation Management System
"""

from datetime import date
import re
import mysql.connector

from database.connection import get_db_connection


VALID_BLOOD_TYPES = {
    "A+", "A-",
    "B+", "B-",
    "AB+", "AB-",
    "O+", "O-"
}


# ===========================================
# Helper Functions
# ===========================================

def calculate_age(date_of_birth):
    """Calculate donor age from date of birth."""

    today = date.today()

    return (
        today.year
        - date_of_birth.year
        - (
            (today.month, today.day)
            <
            (date_of_birth.month, date_of_birth.day)
        )
    )


def validate_donor_info(data):

    if len(data["full_name"].strip()) < 2:
        return False, "Invalid full name."

    age = calculate_age(data["date_of_birth"])

    if age < 18:
        return False, "Donor must be at least 18 years old."

    if age > 65:
        return False, "Maximum donor age is 65."

    if data["blood_type"] not in VALID_BLOOD_TYPES:
        return False, "Invalid blood type."

    phone_pattern = r"^\+?[0-9]{10,15}$"

    if not re.match(phone_pattern, data["phone"]):
        return False, "Invalid phone number."

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_pattern, data["email"]):
        return False, "Invalid email."

    return True, ""


# ===========================================
# Register Donor
# ===========================================

def register_donor(data):

    valid, message = validate_donor_info(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor()

    query = """
    INSERT INTO donors
    (
        full_name,
        date_of_birth,
        blood_type,
        phone,
        email,
        district,
        is_available
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s
    )
    """

    cursor.execute(

        query,

        (

            data["full_name"],

            data["date_of_birth"],

            data["blood_type"],

            data["phone"],

            data["email"],

            data["district"],

            data.get("is_available", True)

        )

    )

    connection.commit()

    donor_id = cursor.lastrowid

    cursor.close()

    connection.close()

    return {

        "success": True,

        "message": "Donor registered successfully.",

        "donor_id": donor_id

    }


# ===========================================
# Get One Donor
# ===========================================

def get_donor_by_id(donor_id):

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(

        """
        SELECT *
        FROM donors
        WHERE donor_id=%s
        """,

        (donor_id,)

    )

    donor = cursor.fetchone()

    cursor.close()

    connection.close()

    if donor:

        return {

            "success": True,

            "data": donor

        }

    return {

        "success": False,

        "message": "Donor not found."

    }


# ===========================================
# Get All Donors
# ===========================================

def get_all_donors():

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *

        FROM donors

        ORDER BY full_name

    """)

    donors = cursor.fetchall()

    cursor.close()

    connection.close()

    return {

        "success": True,

        "data": donors

    }


# ===========================================
# Update Donor
# ===========================================

def update_donor(donor_id, data):

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """

    UPDATE donors

    SET

        full_name=%s,

        date_of_birth=%s,

        blood_type=%s,

        phone=%s,

        email=%s,

        district=%s,

        is_available=%s

    WHERE donor_id=%s

    """

    cursor.execute(

        query,

        (

            data["full_name"],

            data["date_of_birth"],

            data["blood_type"],

            data["phone"],

            data["email"],

            data["district"],

            data["is_available"],

            donor_id

        )

    )

    connection.commit()

    cursor.close()

    connection.close()

    return {

        "success": True,

        "message": "Donor updated successfully."

    }
