"""Donor management workflow for the LifeLink Blood Donation Management System.

Owned by Member 3. Implements:
    - Donor Registration
    - View Profile
    - Update Profile
    - Change Availability
    - Donor Information Validation

NOTE (Day 1 skeleton): Database access is owned by Member 4. Once
database/connection.py exposes a connection helper, replace the `# TODO`
markers below with real calls (parameterized queries only, never
string-format SQL, never store passwords in plain text).
"""

from datetime import date
from typing import Optional

from donors.donor import Donor

VALID_BLOOD_TYPES = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}


def register_donor(
    full_name: str,
    blood_type: str,
    district: str,
    phone_number: str,
    date_of_birth: date,
) -> Donor:
    """Registers a new donor after validating input.

    Args:
        full_name: Donor's full name.
        blood_type: Donor's blood group (e.g. "O+").
        district: District where the donor is located.
        phone_number: Donor's contact number.
        date_of_birth: Donor's date of birth.

    Returns:
        The newly created Donor object (with donor_id populated once the
        database layer is wired in).

    Raises:
        ValueError: If any of the supplied donor information is invalid.
    """
    is_valid, error_message = validate_donor_info(
        full_name, blood_type, district, phone_number, date_of_birth
    )
    if not is_valid:
        raise ValueError(error_message)

    donor = Donor(
        donor_id=None,
        full_name=full_name,
        blood_type=blood_type,
        district=district,
        phone_number=phone_number,
        date_of_birth=date_of_birth,
    )

    # TODO: persist `donor` via database.connection (Member 4) and set
    # donor.donor_id from the inserted row's id.

    return donor


def view_profile(donor_id: int) -> Optional[Donor]:
    """Retrieves a donor's profile by id.

    Args:
        donor_id: The id of the donor to look up.

    Returns:
        The matching Donor object, or None if no donor was found.
    """
    # TODO: fetch the donor row via database.connection and map it to a
    # Donor object.
    raise NotImplementedError("Pending integration with the database module.")


def update_profile(donor_id: int, updated_fields: dict) -> Donor:
    """Updates one or more fields on an existing donor's profile.

    Args:
        donor_id: The id of the donor to update.
        updated_fields: Mapping of field names to their new values (only
            fields present in the Donor model are applied).

    Returns:
        The updated Donor object.

    Raises:
        ValueError: If `updated_fields` contains invalid donor information.
    """
    # TODO: fetch the existing donor, apply and validate updated_fields,
    # then persist via database.connection.
    raise NotImplementedError("Pending integration with the database module.")


def change_availability(donor_id: int, is_available: bool) -> Donor:
    """Updates a donor's availability status.

    Args:
        donor_id: The id of the donor to update.
        is_available: The new availability status.

    Returns:
        The updated Donor object.
    """
    # TODO: persist the availability change via database.connection.
    raise NotImplementedError("Pending integration with the database module.")


def validate_donor_info(
    full_name: str,
    blood_type: str,
    district: str,
    phone_number: str,
    date_of_birth: date,
) -> tuple[bool, Optional[str]]:
    """Validates donor information before registration or an update.

    Args:
        full_name: Donor's full name.
        blood_type: Donor's blood group.
        district: District where the donor is located.
        phone_number: Donor's contact number.
        date_of_birth: Donor's date of birth.

    Returns:
        A tuple of (is_valid, error_message). error_message is None when
        is_valid is True.
    """
    if not full_name or not full_name.strip():
        return False, "Full name is required."

    if blood_type not in VALID_BLOOD_TYPES:
        return False, f"Blood type must be one of {sorted(VALID_BLOOD_TYPES)}."

    if not district or not district.strip():
        return False, "District is required."

    if not phone_number or not phone_number.strip():
        return False, "Phone number is required."

    if date_of_birth >= date.today():
        return False, "Date of birth must be in the past."

    return True, None