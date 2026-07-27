"""
Report Generator
LifeLink Blood Donation Management System

Generates statistics and summaries
from the database.
"""


from database.connection import get_db_connection


# ===========================================
# Total Donors
# ===========================================

def get_total_donors():
    """
    Returns the total number of registered donors.
    """

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM donors
        """
    )

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": total
    }


# ===========================================
# Total Donations
# ===========================================

def get_total_donations():
    """
    Returns total donations recorded.
    """

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM donations
        """
    )

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": total
    }


# ===========================================
# Donors By Blood Type
# ===========================================

def donors_by_blood_type():
    """
    Returns number of donors grouped by blood type.
    """

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            blood_type,
            COUNT(*) AS total
        FROM donors
        GROUP BY blood_type
        ORDER BY total DESC
        """
    )

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": result
    }


# ===========================================
# Donors By District
# ===========================================

def donors_by_district():
    """
    Returns number of donors grouped by district.
    """

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            district,
            COUNT(*) AS total
        FROM donors
        GROUP BY district
        ORDER BY total DESC
        """
    )

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": result
    }


# ===========================================
# Available Donors
# ===========================================

def get_available_donor_count():
    """
    Returns donors currently available.
    """

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM donors
        WHERE is_available = TRUE
        """
    )

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": total
    }


# ===========================================
# Full Dashboard Report
# ===========================================

def generate_dashboard_report():
    """
    Creates a complete system summary.
    """

    return {

        "total_donors": get_total_donors(),

        "total_donations": get_total_donations(),

        "available_donors": get_available_donor_count(),

        "blood_types": donors_by_blood_type(),

        "districts": donors_by_district()

    }


# ===========================================
# Testing
# ===========================================

if __name__ == "__main__":

    report = generate_dashboard_report()

    print(report)