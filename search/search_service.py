"""
Search Service
LifeLink Blood Donation Management System

Provides functions for searching donors
by blood type, district, or both.
"""

from database.connection import get_db_connection


# ===========================================
# Search by Blood Type
# ===========================================

def search_by_blood_type(blood_type):

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM donors
    WHERE blood_type = %s
    ORDER BY full_name
    """

    cursor.execute(query, (blood_type,))

    donors = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": donors
    }


# ===========================================
# Search by District
# ===========================================

def search_by_district(district):

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM donors
    WHERE district = %s
    ORDER BY full_name
    """

    cursor.execute(query, (district,))

    donors = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": donors
    }


# ===========================================
# Search by Blood Type and District
# ===========================================

def search_by_blood_type_and_district(blood_type, district):

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM donors
    WHERE blood_type = %s
    AND district = %s
    ORDER BY full_name
    """

    cursor.execute(
        query,
        (blood_type, district)
    )

    donors = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": donors
    }


# ===========================================
# Search by Donor ID
# ===========================================

def search_by_donor_id(donor_id):

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM donors
    WHERE donor_id = %s
    """

    cursor.execute(query, (donor_id,))

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
# Get Eligible Donors
# ===========================================

def get_available_donors():

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM donors
    WHERE is_available = TRUE
    ORDER BY blood_type, full_name
    """

    cursor.execute(query)

    donors = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": donors
    }


# ===========================================
# Testing
# ===========================================

if __name__ == "__main__":

    print(search_by_blood_type("O+"))

    print(search_by_district("Gasabo"))

    print(
        search_by_blood_type_and_district(
            "A+",
            "Kicukiro"
        )
    )