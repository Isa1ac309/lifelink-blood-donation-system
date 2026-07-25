"""Donation management workflow for the LifeLink Blood Donation System.

Owned by Member 4 (Database & Donations). Implements:
    - Record a blood donation (write to MySQL)
    - Update the donor's last_donation_date on each new donation
    - Retrieve a donor's donation history
    - Retrieve individual / all donation records

All database access goes through ``database.connection.get_connection``.
Every query is parameterized (never string-formatted) to prevent SQL
injection, and recording a donation runs inside a single transaction so
the donation row and the donor's updated last_donation_date either both
persist or neither does.
"""

from datetime import date, datetime
from typing import Optional, Union

import mysql.connector

from database.connection import get_connection

# A standard whole-blood donation is 450 ml. Used as the default volume.
DEFAULT_VOLUME_ML = 450

DateInput = Union[str, date]


def _normalise_date(value: DateInput) -> date:
    """Coerces a date input into a ``datetime.date``.

    Args:
        value: Either a ``datetime.date`` or a "YYYY-MM-DD" string.

    Returns:
        The corresponding ``datetime.date``.

    Raises:
        ValueError: If a string is not in YYYY-MM-DD format.
        TypeError: If value is neither a date nor a string.
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError as error:
            raise ValueError(
                "donation_date must be in YYYY-MM-DD format."
            ) from error
    raise TypeError("donation_date must be a date or a YYYY-MM-DD string.")


def _validate_donation_input(
    donor_id: int,
    donation_date: date,
    volume_ml: int,
) -> Optional[str]:
    """Validates donation fields. Returns an error message, or None if ok."""
    if not isinstance(donor_id, int) or donor_id <= 0:
        return "donor_id must be a positive integer."
    if donation_date > date.today():
        return "donation_date cannot be in the future."
    if not isinstance(volume_ml, int) or volume_ml <= 0:
        return "volume_ml must be a positive integer."
    return None


def record_donation(
    donor_id: int,
    donation_date: DateInput,
    volume_ml: int = DEFAULT_VOLUME_ML,
    location_id: Optional[int] = None,
    notes: Optional[str] = None,
) -> dict:
    """Records a new blood donation and updates the donor's last donation.

    Inserts a row into ``donations`` and, in the same transaction, moves
    the donor's ``last_donation_date`` forward to this donation's date
    (only if the new date is more recent than the stored one, so that
    back-dated entries never rewind a donor's eligibility clock).

    Args:
        donor_id: Id of the donating donor. Must reference an existing
            donor (enforced by a foreign key).
        donation_date: Date of the donation (date object or YYYY-MM-DD).
        volume_ml: Volume collected in millilitres. Defaults to 450.
        location_id: Optional id of the donation location.
        notes: Optional free-text note.

    Returns:
        A result dict:
            {"success": True, "message": ..., "donation_id": int}
        on success, or
            {"success": False, "message": ...}
        on validation failure or a database error.
    """
    try:
        donation_date = _normalise_date(donation_date)
    except (ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    error_message = _validate_donation_input(donor_id, donation_date, volume_ml)
    if error_message:
        return {"success": False, "message": f"Validation failed: {error_message}"}

    insert_query = """
        INSERT INTO donations (donor_id, location_id, donation_date, volume_ml, notes)
        VALUES (%s, %s, %s, %s, %s)
    """
    # Only advance last_donation_date; never move it backwards.
    update_query = """
        UPDATE donors
        SET last_donation_date = %s
        WHERE donor_id = %s
          AND (last_donation_date IS NULL OR last_donation_date < %s)
    """

    connection = None
    cursor = None
    try:
        connection = get_connection()
        connection.autocommit = False  # explicit transaction
        cursor = connection.cursor()

        cursor.execute(
            insert_query,
            (donor_id, location_id, donation_date, volume_ml, notes),
        )
        donation_id = cursor.lastrowid

        cursor.execute(update_query, (donation_date, donor_id, donation_date))

        connection.commit()
        return {
            "success": True,
            "message": "Donation recorded successfully.",
            "donation_id": donation_id,
        }
    except mysql.connector.IntegrityError as error:
        if connection:
            connection.rollback()
        # Raised when donor_id (or location_id) has no matching parent row.
        return {
            "success": False,
            "message": f"Foreign key error (unknown donor or location): {error}",
        }
    except mysql.connector.Error as error:
        if connection:
            connection.rollback()
        return {"success": False, "message": f"Database error: {error}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_donation_history(donor_id: int) -> dict:
    """Retrieves all donations for a donor, most recent first.

    Args:
        donor_id: Id of the donor whose history is requested.

    Returns:
        {"success": True, "data": [ ... rows ... ]} on success, where each
        row includes the location name (or None), or
        {"success": False, "message": ...} on error.
    """
    if not isinstance(donor_id, int) or donor_id <= 0:
        return {"success": False, "message": "donor_id must be a positive integer."}

    query = """
        SELECT
            d.donation_id,
            d.donor_id,
            d.donation_date,
            d.volume_ml,
            d.location_id,
            l.name AS location_name,
            d.notes,
            d.created_at
        FROM donations AS d
        LEFT JOIN donation_locations AS l ON d.location_id = l.location_id
        WHERE d.donor_id = %s
        ORDER BY d.donation_date DESC, d.donation_id DESC
    """

    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (donor_id,))
        return {"success": True, "data": cursor.fetchall()}
    except mysql.connector.Error as error:
        return {"success": False, "message": f"Database error: {error}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_donation(donation_id: int) -> dict:
    """Retrieves a single donation record by its id.

    Args:
        donation_id: Id of the donation to fetch.

    Returns:
        {"success": True, "data": {...}} if found,
        {"success": False, "message": ...} if not found or on error.
    """
    if not isinstance(donation_id, int) or donation_id <= 0:
        return {"success": False, "message": "donation_id must be a positive integer."}

    query = """
        SELECT donation_id, donor_id, location_id, donation_date,
               volume_ml, notes, created_at
        FROM donations
        WHERE donation_id = %s
    """

    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (donation_id,))
        row = cursor.fetchone()
        if row is None:
            return {
                "success": False,
                "message": f"No donation found with id {donation_id}.",
            }
        return {"success": True, "data": row}
    except mysql.connector.Error as error:
        return {"success": False, "message": f"Database error: {error}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_all_donations() -> dict:
    """Retrieves every donation joined to its donor (for reporting).

    Provided for Member 6's reporting module (donation history / activity
    reports). Returns donor name and blood type alongside each donation.

    Returns:
        {"success": True, "data": [ ... rows ... ]} on success, or
        {"success": False, "message": ...} on error.
    """
    query = """
        SELECT
            d.donation_id,
            d.donor_id,
            dn.full_name,
            dn.blood_type,
            d.donation_date,
            d.volume_ml,
            l.name AS location_name
        FROM donations AS d
        JOIN donors AS dn ON d.donor_id = dn.donor_id
        LEFT JOIN donation_locations AS l ON d.location_id = l.location_id
        ORDER BY d.donation_date DESC, d.donation_id DESC
    """

    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        return {"success": True, "data": cursor.fetchall()}
    except mysql.connector.Error as error:
        return {"success": False, "message": f"Database error: {error}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
