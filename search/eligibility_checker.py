"""
Eligibility checking module.

Determines whether a donor is eligible
to donate blood.
"""

from datetime import date


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
    pass


def days_until_eligible(last_donation_date):
    """
    Calculate the remaining days until
    the donor becomes eligible again.

    Args:
        last_donation_date (date): Date of previous donation.

    Returns:
        int: Number of remaining days.
    """
    pass
