"""
Donor Management Service
Handles registration, retrieval, updating, and validation for donor records in MySQL.
"""

import re
import mysql.connector
from database.connection import get_db_connection


def validate_donor_info(data: dict) -> tuple[bool, str]:
    """
    Validates donor profile data before database insertion or update.
    """
    if not data.get("full_name") or len(data["full_name"].strip()) < 2:
        return False, "Full name must be at least 2 characters long."

    age = data.get("age")
    if age is None or not isinstance(age, int) or not (18 <= age <= 65):
        return False, "Donor age must be between 18 and 65 years."

    valid_blood_types = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
    if data.get("blood_type") not in valid_blood_types:
        return False, f"Invalid blood type. Must be one of: {', '.join(valid_blood_types)}"

    phone_pattern = r"^\+?[0-9]{10,15}$"
    if not data.get("phone") or not re.match(phone_pattern, data["phone"]):
        return False, "Invalid phone number. Provide a valid 10 to 15 digit number."

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not data.get("email") or not re.match(email_pattern, str(data["email"])):
        return False, "Invalid email address format."

    if not data.get("district") or len(data["district"].strip()) < 2:
        return False, "District name is required."

    return True, ""


def register_donor(donor_data: dict) -> dict:
    """
    Registers a new donor into the MySQL database after validation.
    """
    is_valid, error_msg = validate_donor_info(donor_data)
    if not is_valid:
        return {"success": False, "message": f"Validation failed: {error_msg}"}

    connection = get_db_connection()
    if not connection:
        return {"success": False, "message": "Database connection failed."}

    query = """
        INSERT INTO donors (full_name, age, blood_type, phone, email, district, is_available)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        donor_data["full_name"].strip(),
        donor_data["age"],
        donor_data["blood_type"],
        donor_data["phone"].strip(),
        donor_data["email"].strip().lower(),
        donor_data["district"].strip(),
        donor_data.get("is_available", True),
    )

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        donor_id = cursor.lastrowid
        return {
            "success": True,
            "message": "Donor registered successfully.",
            "donor_id": donor_id,
        }
    except mysql.connector.Error as err:
        return {"success": False, "message": f"Database error: {err}"}
    finally:
        cursor.close()
        connection.close()


def view_donor_profile(donor_id: int) -> dict:
    """
    Retrieves a single donor profile from MySQL by ID.
    """
    connection = get_db_connection()
    if not connection:
        return {"success": False, "message": "Database connection failed."}

    query = "SELECT donor_id, full_name, age, blood_type, phone, email, district, is_available, last_donation_date FROM donors WHERE donor_id = %s"

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (donor_id,))
        donor = cursor.fetchone()

        if not donor:
            return {"success": False, "message": f"Donor with ID {donor_id} not found."}

        return {"success": True, "data": donor}
    except mysql.connector.Error as err:
        return {"success": False, "message": f"Database error: {err}"}
    finally:
        cursor.close()
        connection.close()


def update_donor_profile(donor_id: int, update_data: dict) -> dict:
    """
    Updates an existing donor's information in MySQL after validation.
    """
    existing = view_donor_profile(donor_id)
    if not existing["success"]:
        return existing

    merged_data = existing["data"]
    merged_data.update(update_data)

    is_valid, error_msg = validate_donor_info(merged_data)
    if not is_valid:
        return {"success": False, "message": f"Validation failed: {error_msg}"}

    connection = get_db_connection()
    if not connection:
        return {"success": False, "message": "Database connection failed."}

    query = """
        UPDATE donors
        SET full_name = %s, age = %s, blood_type = %s, phone = %s, email = %s, district = %s, is_available = %s
        WHERE donor_id = %s
    """
    params = (
        merged_data["full_name"].strip(),
        merged_data["age"],
        merged_data["blood_type"],
        merged_data["phone"].strip(),
        merged_data["email"].strip().lower(),
        merged_data["district"].strip(),
        merged_data["is_available"],
        donor_id,
    )

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return {"success": True, "message": "Donor profile updated successfully."}
    except mysql.connector.Error as err:
        return {"success": False, "message": f"Database error: {err}"}
    finally:
        cursor.close()
        connection.close()
