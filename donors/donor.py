"""Donor data model for the LifeLink Blood Donation Management System.

Owned by Member 3 (Donor Registration & Donor Management).
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Donor:
    """Represents a single blood donor record.

    Attributes:
        donor_id: Primary key, assigned by the database (None until saved).
        full_name: Donor's full name.
        blood_type: One of the standard blood group strings (e.g. "O+").
        district: District where the donor is located, used for search.
        phone_number: Contact number for the donor.
        date_of_birth: Donor's date of birth, stored as YYYY-MM-DD.
        last_donation_date: Date of the donor's most recent donation, or
            None if the donor has never donated.
        is_available: Whether the donor currently marks themselves as
            available to donate.
    """

    donor_id: Optional[int]
    full_name: str
    blood_type: str
    district: str
    phone_number: str
    date_of_birth: date
    last_donation_date: Optional[date] = None
    is_available: bool = True