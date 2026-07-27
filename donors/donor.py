"""
Donor Model
LifeLink Blood Donation Management System

Represents a single donor.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Donor:
    """
    Represents a blood donor.
    """

    donor_id: Optional[int] = None

    full_name: str = ""

    date_of_birth: date = None

    blood_type: str = ""

    phone: str = ""

    email: str = ""

    district: str = ""

    last_donation_date: Optional[date] = None

    is_available: bool = True

    created_at: Optional[date] = None
