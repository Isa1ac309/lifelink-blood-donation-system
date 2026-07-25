"""Manual verification harness for Member 4's database + donation work.

Run from the repo root with a MySQL server available and a .env file:

    python -m tests.verify_donation_service

It proves, against a REAL MySQL database (not in-memory):
  1. The schema applies and data persists across separate connections.
  2. Recording a donation writes a row to the donations table.
  3. The donor's last_donation_date is updated on each new donation.
  4. Donation history retrieval returns the stored rows.
  5. The foreign key rejects a donation for a non-existent donor.
  6. ON DELETE RESTRICT blocks deleting a donor who has donations.

This is a developer smoke test, not part of the shipped app flow.
"""

from datetime import date

from database.connection import get_connection, init_database
from donations import donation_service

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
results = []


def check(label, condition):
    results.append(bool(condition))
    print(f"  [{PASS if condition else FAIL}] {label}")
    return condition


def fetch_last_donation_date(donor_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT last_donation_date FROM donors WHERE donor_id = %s",
            (donor_id,),
        )
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
        conn.close()


def seed_donor():
    """Inserts one donor directly and returns its id."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO donors
               (full_name, blood_type, district, phone, email, date_of_birth)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            ("Test Donor", "O+", "Gasabo", "+250788000111",
             "test@example.com", date(1995, 5, 20)),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()


def cleanup(donor_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM donations WHERE donor_id = %s", (donor_id,))
        cur.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def main():
    print("Applying schema...")
    init_database()

    donor_id = seed_donor()
    print(f"Seeded donor_id = {donor_id}\n")

    print("1) Record a donation (writes to MySQL):")
    r1 = donation_service.record_donation(donor_id, "2026-03-01", volume_ml=450)
    check("record_donation returned success", r1.get("success"))
    first_id = r1.get("donation_id")
    check("a donation_id was assigned by the DB", isinstance(first_id, int))

    print("2) Donor's last_donation_date updated:")
    check("last_donation_date == 2026-03-01",
          fetch_last_donation_date(donor_id) == date(2026, 3, 1))

    print("3) Record a later donation advances last_donation_date:")
    donation_service.record_donation(donor_id, "2026-06-15")
    check("last_donation_date advanced to 2026-06-15",
          fetch_last_donation_date(donor_id) == date(2026, 6, 15))

    print("4) A back-dated donation does NOT rewind last_donation_date:")
    donation_service.record_donation(donor_id, "2026-01-10")
    check("last_donation_date stays 2026-06-15",
          fetch_last_donation_date(donor_id) == date(2026, 6, 15))

    print("5) Data persists on a brand-new connection (not in memory):")
    hist = donation_service.get_donation_history(donor_id)
    check("history query succeeded", hist.get("success"))
    check("3 donations persisted", len(hist.get("data", [])) == 3)

    print("6) Foreign key rejects a donation for a non-existent donor:")
    bad = donation_service.record_donation(999999, "2026-03-01")
    check("record_donation reported failure", not bad.get("success"))
    check("failure message mentions foreign key",
          "foreign key" in bad.get("message", "").lower())

    print("7) ON DELETE RESTRICT blocks deleting a donor with donations:")
    blocked = False
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
        conn.commit()
    except Exception:  # noqa: BLE001 - we expect an IntegrityError here
        conn.rollback()
        blocked = True
    finally:
        cur.close()
        conn.close()
    check("delete of donor-with-donations was blocked", blocked)

    cleanup(donor_id)

    print("\n" + "=" * 50)
    total, passed = len(results), sum(results)
    print(f"RESULT: {passed}/{total} checks passed")
    print("=" * 50)
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
