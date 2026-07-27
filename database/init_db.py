"""Database initialization script for the LifeLink Blood Donation System.

Owned by Gatete Irene (Database & Donations). Covers the guide's
"database initialization scripts" responsibility.

Usage (from the repo root):
    python -m database.init_db           # create the schema only
    python -m database.init_db --seed    # also seed reference locations

Applying the schema is safe to repeat (CREATE ... IF NOT EXISTS). Seeding
only inserts reference donation_locations that are not already present, so
it is also safe to run more than once. It does not touch donor, donation,
or administrator data (owned by other members).
"""

import sys

import mysql.connector

from database.connection import get_connection, init_database

# Reference donation centres used to bootstrap the donations foreign key.
# donation_locations is Member 5's data domain; these are only harmless
# reference rows so donation recording can be exercised end to end.
REFERENCE_LOCATIONS = [
    ("Kigali Central Blood Bank", "Nyarugenge", "KN 4 Ave, Kigali"),
    ("Kacyiru Health Center", "Gasabo", "KG 7 Ave, Kacyiru"),
    ("Remera Donation Point", "Gasabo", "KK 15 Rd, Remera"),
    ("Huye Regional Center", "Huye", "Huye District Hospital"),
]


def seed_reference_locations() -> int:
    """Inserts reference donation_locations that do not already exist.

    Returns:
        The number of new location rows inserted.
    """
    insert_query = """
        INSERT INTO donation_locations (name, district, address)
        SELECT %s, %s, 
        WHERE NOT EXISTS (
            SELECT 1 FROM donation_locations WHERE name = %s
        )
    """
    connection = None
    cursor = None
    inserted = 0
    try:
        connection = get_connection()
        cursor = connection.cursor()
        for name, district, address in REFERENCE_LOCATIONS:
            cursor.execute(insert_query, (name, district, address, name))
            inserted += cursor.rowcount
        connection.commit()
        return inserted
    except mysql.connector.Error as error:
        if connection:
            connection.rollback()
        print(f"[init_db] Failed to seed locations: {error}")
        return 0
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main(seed: bool = False) -> None:
    """Runs schema creation and, optionally, reference seeding.

    Args:
        seed: When True, also inserts reference donation_locations.
    """
    init_database()
    if seed:
        count = seed_reference_locations()
        print(f"[init_db] Seeded {count} new donation location(s).")
    print("[init_db] Database initialization complete.")


if __name__ == "__main__":
    main(seed="--seed" in sys.argv[1:])
