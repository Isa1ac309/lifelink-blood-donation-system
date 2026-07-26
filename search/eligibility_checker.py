"""
Eligibility Checker
LifeLink Blood Donation Management System

Determines whether a donor is eligible
to donate blood based on the 56-day rule.
"""

from datetime import date, datetime

# Minimum waiting period between donations
ELIGIBILITY_DAYS = 56


def days_until_eligible(last_donation_date):
    """
    Returns the number of days remaining
    before the donor can donate again.

    Accepts either:
        - datetime.date
        - "YYYY-MM-DD" string
        - None
    """

    # Never donated before
    if last_donation_date is None:
        return 0

    # Convert string to date
    if isinstance(last_donation_date, str):

        try:
            last_donation_date = datetime.strptime(
                last_donation_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            raise ValueError(
                "Date must be in YYYY-MM-DD format."
            )

    if not isinstance(last_donation_date, date):

        raise TypeError(
            "last_donation_date must be a date object."
        )

    today = date.today()

    if last_donation_date > today:

        raise ValueError(
            "Donation date cannot be in the future."
        )

    days_passed = (today - last_donation_date).days

    remaining = ELIGIBILITY_DAYS - days_passed

    return max(0, remaining)


def is_eligible(last_donation_date):
    """
    Returns True if donor may donate today.
    """

    return days_until_eligible(last_donation_date) == 0


def eligibility_message(last_donation_date):
    """
    Human-readable eligibility result.
    """

    remaining = days_until_eligible(last_donation_date)

    if remaining == 0:

        return "Eligible to donate."

    return (
        f"Not eligible. "
        f"Wait {remaining} more day(s)."
    )


# ------------------------------------------
# Testing
# ------------------------------------------

if __name__ == "__main__":

    print(is_eligible(None))

    print(eligibility_message(None))

    print(
        eligibility_message(
            "2026-05-01"
        )
    )