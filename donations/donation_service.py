"""
Donation Service
LifeLink Blood Donation Management System

Handles blood donation recording.
"""

from datetime import date

from database.connection import get_db_connection
from search.eligibility_checker import is_eligible


# ===========================================
# Helper Functions
# ===========================================

def donor_exists(donor_id):
    """Check if a donor exists."""

    connection = get_db_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    cursor.execute(
        "SELECT donor_id FROM donors WHERE donor_id=%s",
        (donor_id,)
    )

    exists = cursor.fetchone() is not None

    cursor.close()
    connection.close()

    return exists


def location_exists(location_id):
    """Check if a donation location exists."""

    connection = get_db_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    cursor.execute(
        "SELECT location_id FROM donation_locations WHERE location_id=%s",
        (location_id,)
    )

    exists = cursor.fetchone() is not None

    cursor.close()
    connection.close()

    return exists


# ===========================================
# Record Donation
# ===========================================

def record_donation(donor_id, location_id, donation_date=None, volume_ml=450):
    """
    Records a blood donation and updates the donor.
    """

    if donation_date is None:
        donation_date = date.today()

    if not donor_exists(donor_id):
        return {
            "success": False,
            "message": "Donor not found."
        }

    if not location_exists(location_id):
        return {
            "success": False,
            "message": "Donation location not found."
        }

    connection = get_db_connection()

    if not connection:
        return {
            "success": False,
            "message": "Database connection failed."
        }

    cursor = connection.cursor(dictionary=True)

    # Get donor information
    cursor.execute(
        """
        SELECT last_donation_date
        FROM donors
        WHERE donor_id=%s
        """,
        (donor_id,)
    )

    donor = cursor.fetchone()

    # Check eligibility
    if donor["last_donation_date"] is not None:

        if not is_eligible(donor["last_donation_date"]):

            cursor.close()
            connection.close()

            return {
                "success": False,
                "message": "Donor is not yet eligible."
            }

    # Record donation
    cursor.execute(
        """
        INSERT INTO donations
        (
            donor_id,
            location_id,
            donation_date,
            volume_ml
        )
        VALUES
        (%s,%s,%s,%s)
        """,
        (
            donor_id,
            location_id,
            donation_date,
            volume_ml
        )
    )

    # Update donor
    cursor.execute(
        """
        UPDATE donors
        SET
            last_donation_date=%s,
            is_available=FALSE
        WHERE donor_id=%s
        """,
        (
            donation_date,
            donor_id
        )
    )

    connection.commit()

    donation_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return {
        "success": True,
        "message": "Donation recorded successfully.",
        "donation_id": donation_id
    }


# ===========================================
# Donation History
# ===========================================

def get_donation_history(donor_id):
    """
    Returns donation history for a donor.
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
            d.donation_id,
            d.donation_date,
            d.volume_ml,
            l.location_name,
            l.district
        FROM donations d
        JOIN donation_locations l
            ON d.location_id = l.location_id
        WHERE d.donor_id=%s
        ORDER BY d.donation_date DESC
        """,
        (donor_id,)
    )

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "success": True,
        "data": history
    }


# ===========================================
# Testing
# ===========================================

if __name__ == "__main__":

    print(
        record_donation(
            donor_id=1,
            location_id=1
        )
    )

    print(
        get_donation_history(1)
    )