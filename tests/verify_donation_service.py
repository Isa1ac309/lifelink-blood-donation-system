"""
Simple verification test for LifeLink Donation Service.

Run:
    python -m tests.verify_donation_service
"""

from datetime import date

from database.connection import get_db_connection
from donations.donation_service import get_donation_history, record_donation


def check(label, condition):
    """Print the result of a test check."""
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    return condition


def create_test_data():
    """Create a temporary donor and donation location."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO donors
        (full_name, date_of_birth, blood_type, phone, email, district)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            "Test Donor", date(1995, 5, 20), "O+",
            "+250788000111", "test_donor@example.com", "Gasabo",
        ),
    )
    donor_id = cur.lastrowid

    cur.execute(
        """INSERT INTO donation_locations
        (location_name, district)
        VALUES (%s, %s)""",
        ("Test Location", "Gasabo"),
    )
    location_id = cur.lastrowid

    conn.commit()
    cur.close()
    conn.close()
    return donor_id, location_id


def get_last_donation_date(donor_id):
    """Return a donor's last donation date."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT last_donation_date FROM donors WHERE donor_id = %s",
        (donor_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None


def cleanup(donor_id, location_id):
    """Remove temporary test data."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM donations WHERE donor_id = %s", (donor_id,))
    cur.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
    cur.execute(
        "DELETE FROM donation_locations WHERE location_id = %s",
        (location_id,),
    )
    conn.commit()
    cur.close()
    conn.close()


def main():
    """Run donation service verification tests."""
    print("\n" + "=" * 55)
    print("       LIFELINK DONATION SERVICE TEST")
    print("=" * 55)

    print("\n1) Database connection")
    conn = get_db_connection()
    if not conn:
        print("  [FAIL] MySQL connection failed")
        return 1
    print("  [PASS] MySQL connection successful")
    conn.close()

    print("\n2) Creating test data")
    donor_id, location_id = create_test_data()
    print(f"  [PASS] Test donor created (ID: {donor_id})")
    print(f"  [PASS] Test location created (ID: {location_id})")

    print("\n3) Recording donation")
    donation = record_donation(
        donor_id, location_id, "2026-07-20", 450
    )
    checks = [
        check("Donation recorded successfully",
              donation.get("success") is True),
        check("Donation ID was created",
              isinstance(donation.get("donation_id"), int)),
    ]

    print("\n4) Checking donor update")
    checks.append(
        check(
            "last_donation_date was updated",
            get_last_donation_date(donor_id) == date(2026, 7, 20),
        )
    )

    print("\n5) Checking donation history")
    history = get_donation_history(donor_id)
    checks.extend([
        check("Donation history query succeeded",
              history.get("success") is True),
        check("One donation appears in history",
              len(history.get("data", [])) == 1),
    ])

    print("\n6) Testing invalid donor")
    invalid = record_donation(999999, location_id, "2026-07-21")
    checks.append(
        check("Invalid donor was rejected",
              invalid.get("success") is False)
    )

    print("\n7) Cleaning up")
    cleanup(donor_id, location_id)
    print("  [PASS] Test data removed")

    passed = sum(checks)
    total = len(checks)

    print("\n" + "=" * 55)
    print(f"RESULT: {passed}/{total} CHECKS PASSED")
    print("=" * 55)

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())