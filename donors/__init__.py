"""Donor management package for the LifeLink Blood Donation Management System.

Owned by Member 3. Re-exports the public donor CRUD interface so other
modules can do:

    from donors import Donor, register_donor, view_profile
"""

from donors.donor import Donor
from donors.donor_service import (
    change_availability,
    register_donor,
    update_profile,
    validate_donor_info,
    view_profile,
)

__all__ = [
    "Donor",
    "register_donor",
    "view_profile",
    "update_profile",
    "change_availability",
    "validate_donor_info",
]