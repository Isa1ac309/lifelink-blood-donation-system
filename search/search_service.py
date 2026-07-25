"""
Search services for finding donors.

This module contains functions for searching donors
using different criteria.
"""

import mysql.connector

from database.connection import get_db_connection


def search_by_blood_type(blood_type):
    """
    Search donors by blood type.

    Args:
        blood_type (str): Blood group to search for.

    Returns:
        list: Matching donor records.
    """

    if not blood_type:
        return []

    blood_type = blood_type.strip().upper()
    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                donor_id,
                first_name,
                last_name,
                blood_type,
                district,
                phone
            FROM donors
            WHERE blood_type = %s
        """

        cursor.execute(query, (blood_type,))
        donors = cursor.fetchall()
        return donors

    except mysql.connector.Error as error:
        print(f"Database Error: {error}")
        return []
    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def search_by_district(district):
    """
    Search donors by district.

    Args:
        district (str): District name.

    Returns:
        list: Matching donor records.
    """

    if not district:
        return []

    district = district.strip().title()
    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                donor_id,
                first_name,
                last_name,
                blood_type,
                district,
                phone
            FROM donors
            WHERE district = %s
        """

        cursor.execute(query, (district,))
        donors = cursor.fetchall()
        return donors

    except mysql.connector.Error as error:
        print(f"Database Error: {error}")
        return []
    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def search_by_blood_type_and_district(blood_type, district):
    """
    Search donors by both blood type and district.

    Args:
        blood_type (str): Blood group.
        district (str): District.

    Returns:
        list: Matching donor records.

    """

    if not blood_type or not district:
        return []

    blood_type = blood_type.strip().upper()
    district = district.strip().title()

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT
                donor_id,
                first_name,
                last_name,
                blood_type,
                district,
                phone
            FROM donors
            WHERE blood_type = %s
            AND district = %s
        """

        cursor.execute(query, (blood_type, district))
        donors = cursor.fetchall()

        return donors
    except mysql.connector.Error as error:
        print(f"Database Error: {error}")
        return []
    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()