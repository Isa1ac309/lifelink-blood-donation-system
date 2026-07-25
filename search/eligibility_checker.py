"""
Eligibility checking module.

Determines whether a donor is eligible
to donate blood.
"""


from datetime import date, datetime
# Minimum of days one spend before the next donation

ELIGIBILITY_DAYS = 56


def is_eligible(last_donation_date):
    """
    Determine whether a donor is eligible.

    A donor is eligible if at least
    56 days have passed since their
    last donation.

    Args:
        last_donation_date (date): Date of the previous donation.

    Returns:
        bool: True if eligible, False otherwise.
    """
    return days_until_eligible(last_donation_date) == 0


def days_until_eligible(last_donation_date):
    """
    Calculate the remaining days until
    the donor becomes eligible again.

    Args:
        last_donation_date (date): Date of previous donation.

    Returns:
        int: Number of remaining days.
    """
    last_donation_date = last_donation_date.strip()
    # We will first validate the input. ino our case is the last_donation_date
    if isinstance(last_donation_date, str):

        if not last_donation_date.strip():
            raise ValueError("Date cannot be empty.")

        try:
            last_donation_date = datetime.strptime(
                last_donation_date,
                "%d/%m/%Y"
            ).date()
        except ValueError as error:
            raise ValueError(str(error)) from error

    if last_donation_date is None:
        raise TypeError("Last donation date is not provided!")
    if not isinstance(last_donation_date, date):
        raise TypeError(
    "Date must be a date object or DD/MM/YYYY format."
)
    today = date.today()
    if last_donation_date > today:
        raise ValueError("Date cannot be in the future.")
    # we calculate the days passed since the last donation
    days_passed = (today - last_donation_date).days
    # we calculate the remaining days
    remaining_days = ELIGIBILITY_DAYS - days_passed
    return max(0, remaining_days)


