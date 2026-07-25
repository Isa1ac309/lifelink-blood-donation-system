"""Reporting module for the LifeLink Blood Donation System.

Owned by Member 4 (Database & Donations).

Generates the five required reports directly from MySQL:
    1. Blood group distribution   -> blood_group_distribution()
    2. Eligible donors            -> eligible_donors()
    3. Donation history           -> donation_history()
    4. Donation activity          -> donation_activity()
    5. Emergency donor availability -> emergency_donor_availability()

Each generate_* function returns a result dict:
    {"success": True, "data": [ ...rows... ]}
    {"success": False, "message": "..."}

Data access goes through database.connection.get_connection and reuses
donations.donation_service where it already provides what a report needs.
All queries are parameterized / static (no string-built SQL). Donor
eligibility uses the 56-day rule computed in SQL so it always reflects the
current date.
"""

import mysql.connector

from database.connection import get_connection
from donations import donation_service

# A donor may donate again once at least this many days have passed.
ELIGIBILITY_DAYS = 56


def _run_query(query: str, params: tuple = None) -> dict:
    """Runs a read-only query and returns rows as a result dict.

    Args:
        query: A SELECT statement using %s placeholders.
        params: Values to bind, or None. When None, the connector performs
            no % substitution, so literal % in the SQL (e.g. the '%Y-%m'
            in DATE_FORMAT) is left untouched.

    Returns:
        {"success": True, "data": [dict, ...]} or
        {"success": False, "message": "..."}.
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return {"success": True, "data": cursor.fetchall()}
    except mysql.connector.Error as error:
        return {"success": False, "message": f"Database error: {error}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def blood_group_distribution() -> dict:
    """Report 1: number of registered donors per blood group.

    Returns:
        Result dict whose data is a list of
        {"blood_type": str, "donor_count": int}, ordered by blood type.
    """
    query = """
        SELECT blood_type, COUNT(*) AS donor_count
        FROM donors
        GROUP BY blood_type
        ORDER BY blood_type
    """
    return _run_query(query)


def eligible_donors() -> dict:
    """Report 2: donors currently eligible to donate (56-day rule).

    A donor is eligible when they have never donated, or their last
    donation was at least 56 days ago.

    Returns:
        Result dict whose data is a list of donor rows (id, name, blood
        type, district, phone, last_donation_date), ordered by blood type.
    """
    query = """
        SELECT
            donor_id,
            full_name,
            blood_type,
            district,
            phone,
            last_donation_date
        FROM donors
        WHERE last_donation_date IS NULL
           OR DATEDIFF(CURDATE(), last_donation_date) >= %s
        ORDER BY blood_type, full_name
    """
    return _run_query(query, (ELIGIBILITY_DAYS,))


def donation_history() -> dict:
    """Report 3: full donation history across all donors.

    Reuses donation_service.get_all_donations so the reporting and
    donation modules stay consistent.

    Returns:
        Result dict whose data is a list of donation rows joined to the
        donor's name and blood type, most recent first.
    """
    return donation_service.get_all_donations()


def donation_activity() -> dict:
    """Report 4: donation activity aggregated by calendar month.

    Returns:
        Result dict whose data is a list of
        {"month": "YYYY-MM", "donations": int, "total_volume_ml": int},
        oldest month first.
    """
    query = """
        SELECT
            DATE_FORMAT(donation_date, '%Y-%m') AS month,
            COUNT(*)        AS donations,
            SUM(volume_ml)  AS total_volume_ml
        FROM donations
        GROUP BY month
        ORDER BY month
    """
    return _run_query(query)


def emergency_donor_availability() -> dict:
    """Report 5: donors available AND eligible right now, by blood group.

    For emergencies: counts donors who mark themselves available and also
    satisfy the 56-day eligibility rule, grouped by blood type.

    Returns:
        Result dict whose data is a list of
        {"blood_type": str, "available_eligible_donors": int}.
    """
    query = """
        SELECT
            blood_type,
            COUNT(*) AS available_eligible_donors
        FROM donors
        WHERE is_available = TRUE
          AND (last_donation_date IS NULL
               OR DATEDIFF(CURDATE(), last_donation_date) >= %s)
        GROUP BY blood_type
        ORDER BY blood_type
    """
    return _run_query(query, (ELIGIBILITY_DAYS,))


def render_report(title: str, result: dict) -> str:
    """Formats a report result as a simple text table for the CLI.

    Args:
        title: Heading to display above the table.
        result: A result dict returned by one of the report functions.

    Returns:
        A printable string. If the report failed, returns the error; if it
        has no rows, says so.
    """
    lines = [title, "=" * len(title)]
    if not result.get("success"):
        lines.append(f"Error: {result.get('message', 'unknown error')}")
        return "\n".join(lines)

    rows = result.get("data", [])
    if not rows:
        lines.append("(no data)")
        return "\n".join(lines)

    headers = list(rows[0].keys())
    widths = {
        h: max(len(str(h)), max(len(str(r[h])) for r in rows))
        for h in headers
    }
    lines.append("  ".join(str(h).ljust(widths[h]) for h in headers))
    lines.append("  ".join("-" * widths[h] for h in headers))
    for row in rows:
        lines.append("  ".join(str(row[h]).ljust(widths[h]) for h in headers))
    return "\n".join(lines)


def generate_all_reports() -> str:
    """Builds and formats all five reports as one text block.

    Returns:
        The concatenated, printable text of every report. Suitable for the
        main CLI's "Generate Reports" option.
    """
    sections = [
        render_report("1. Blood Group Distribution", blood_group_distribution()),
        render_report("2. Eligible Donors", eligible_donors()),
        render_report("3. Donation History", donation_history()),
        render_report("4. Donation Activity (by month)", donation_activity()),
        render_report(
            "5. Emergency Donor Availability", emergency_donor_availability()
        ),
    ]
    return "\n\n".join(sections)


if __name__ == "__main__":
    # Convenience: `python -m reports.report_generator` prints every report.
    print(generate_all_reports())
