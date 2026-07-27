"""
LifeLink Blood Donation Management System
Main CLI Application
"""

from datetime import datetime

from auth.authentication import login, register_admin

from donors.donor_service import register_donor, get_donor_by_id,  get_donor_by_name

from donations.donation_service import record_donation,    get_donation_history
from reports.report_generator import generate_dashboard_report

from search.search_service import (
    search_by_blood_type,
    search_by_district,
    search_by_donor_id
)


# ============================================================
# Helper Functions
# ============================================================

def header(title):
    print("\n" + "=" * 55)
    print(title.center(55))
    print("=" * 55)


def pause():
    input("\nPress Enter to continue...")


def success(message):
    print(f"\n[+] {message}")


def error(message):
    print(f"\n[!] {message}")


# ============================================================
# Administrator Login
# ============================================================

def administrator_login():

    header("ADMINISTRATOR LOGIN")

    username = input("Username: ").strip()
    password = input("Password: ")

    if not username:
        error("Username cannot be empty.")
        return

    if not password:
        error("Password cannot be empty.")
        return

    result = login(username, password)

    if result.get("success"):

        success("Login successful.")

        admin = result.get("admin")

        if admin:
            administrator_menu(admin)

    else:
        error(
            result.get(
                "message",
                "Login failed."
            )
        )


# ============================================================
# Register New Administrator
# ============================================================

def register_new_administrator():

    header("REGISTER NEW ADMINISTRATOR")

    username = input("Username: ").strip()

    if not username:
        error("Username cannot be empty.")
        return

    password = input("Password: ")

    if not password:
        error("Password cannot be empty.")
        return

    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        error("Passwords do not match.")
        return

    result = register_admin(
        username,
        password
    )

    if result.get("success"):

        success(
            result.get(
                "message",
                "Administrator registered successfully."
            )
        )

    else:

        error(
            result.get(
                "message",
                "Registration failed."
            )
        )


# ============================================================
# Administrator Menu
# ============================================================

def administrator_menu(admin):

    while True:

        header("ADMINISTRATOR MENU")

        print(
            f"Logged in as: "
            f"{admin.get('username')}"
        )

        print()
        print("1. Register New Administrator")
        print("2. Register Donor")
        print("3. Search Donor")
        print("4. Record Donation")
        print("5. Donation History")
        print("6. Reports")
        print("7. Logout")
        print("0. Exit")

        choice = input("\nChoose option: ").strip()

        if choice == "1":

            register_new_administrator()
            pause()

        elif choice == "2":

            register_donor_menu()
            pause()

        elif choice == "3":

            search_donor_menu()

        elif choice == "4":

            record_donation_menu()
            pause()

        elif choice == "5":

            donation_history_menu()
            pause()

        elif choice == "6":

            reports_menu()
            pause()

        elif choice == "7":

            print("\nLogged out successfully.")
            break

        elif choice == "0":

            return

        else:

            error("Invalid option.")
            pause()


# ============================================================
# Register Donor
# ============================================================

def register_donor_menu():

    header("REGISTER DONOR")

    full_name = input("Full name: ").strip()

    if not full_name:
        error("Full name cannot be empty.")
        return

    date_of_birth = input(
        "Date of birth (YYYY-MM-DD): "
    ).strip()

    try:

        date_of_birth = datetime.strptime(
            date_of_birth,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        error("Invalid date. Use YYYY-MM-DD.")
        return

    blood_type = input(
        "Blood type: "
    ).strip().upper()

    if not blood_type:
        error("Blood type cannot be empty.")
        return

    phone = input("Phone: ").strip()

    if not phone:
        error("Phone cannot be empty.")
        return

    email = input("Email: ").strip()

    if not email:
        error("Email cannot be empty.")
        return

    district = input("District: ").strip()

    if not district:
        error("District cannot be empty.")
        return

    data = {
        "full_name": full_name,
        "date_of_birth": date_of_birth,
        "blood_type": blood_type,
        "phone": phone,
        "email": email,
        "district": district,
        "is_available": True
    }

    result = register_donor(data)

    if result.get("success"):

        success(
            result.get(
                "message",
                "Donor registered successfully."
            )
        )

        print(
            f"Donor ID: "
            f"{result.get('donor_id')}"
        )

    else:

        error(
            result.get(
                "message",
                "Donor registration failed."
            )
        )


# ============================================================
# Display One Donor
# ============================================================

def display_donor(donor):

    print("\n" + "-" * 45)

    print(
        f"ID:            "
        f"{donor.get('donor_id')}"
    )

    print(
        f"Name:          "
        f"{donor.get('full_name')}"
    )

    print(
        f"Blood Type:    "
        f"{donor.get('blood_type')}"
    )

    print(
        f"Phone:         "
        f"{donor.get('phone')}"
    )

    print(
        f"Email:         "
        f"{donor.get('email')}"
    )

    print(
        f"District:      "
        f"{donor.get('district')}"
    )

    if donor.get("is_available"):
        print("Available:     Yes")
    else:
        print("Available:     No")

    print(
        f"Last Donation: "
        f"{donor.get('last_donation_date')}"
    )

    print("-" * 45)


# ============================================================
# Display Multiple Donors
# ============================================================

def display_donors(donors):

    if not donors:

        print("\nNo donors found.")
        return

    for donor in donors:

        display_donor(donor)


# ============================================================
# Search Donor Menu
# ============================================================

def search_donor_menu():

    while True:

        header("SEARCH DONOR")

        print("1. Search by Donor ID")
        print("2. Search by Name")
        print("3. Search by Blood Type")
        print("4. Search by District")
        print("0. Back")

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            search_donor_by_id()

        elif choice == "2":

            search_donor_by_name()

        elif choice == "3":

            search_donor_by_blood_type()

        elif choice == "4":

            search_donor_by_district()

        elif choice == "0":

            break

        else:

            error("Invalid option.")

        if choice != "0":
            pause()


# ============================================================
# Search By Donor ID
# ============================================================

def search_donor_by_id():

    donor_id = input(
        "Enter Donor ID: "
    ).strip()

    if not donor_id.isdigit():

        error("Donor ID must be a number.")
        return

    result = search_by_donor_id(
        int(donor_id)
    )

    if result.get("success"):

        display_donor(
            result["data"]
        )

    else:

        error(
            result.get(
                "message",
                "Donor not found."
            )
        )


# ============================================================
# Search By Name
# ============================================================

def search_donor_by_name():

    name = input(
        "Enter donor name: "
    ).strip()

    if not name:

        error("Name cannot be empty.")
        return

    result = get_donor_by_name(name)

    if result.get("success"):

        display_donor(
            result["data"]
        )

        return

    if result.get("data"):

        print("\nMultiple donors found:")

        display_donors(
            result["data"]
        )

        return

    error(
        result.get(
            "message",
            "Donor not found."
        )
    )


# ============================================================
# Search By Blood Type
# ============================================================

def search_donor_by_blood_type():

    blood_type = input(
        "Enter blood type: "
    ).strip().upper()

    if not blood_type:

        error("Blood type cannot be empty.")
        return

    result = search_by_blood_type(
        blood_type
    )

    if not result.get("success"):

        error(
            result.get(
                "message",
                "Search failed."
            )
        )

        return

    display_donors(
        result.get("data", [])
    )


# ============================================================
# Search By District
# ============================================================

def search_donor_by_district():

    district = input(
        "Enter district: "
    ).strip()

    if not district:

        error("District cannot be empty.")
        return

    result = search_by_district(
        district
    )

    if not result.get("success"):

        error(
            result.get(
                "message",
                "Search failed."
            )
        )

        return

    display_donors(
        result.get("data", [])
    )


# ============================================================
# Record Donation
# ============================================================

def record_donation_menu():

    header("RECORD DONATION")

    donor_id = input(
        "Donor ID: "
    ).strip()

    if not donor_id.isdigit():

        error("Donor ID must be a number.")
        return

    location_id = input(
        "Location ID: "
    ).strip()

    if not location_id.isdigit():

        error("Location ID must be a number.")
        return

    donation_date = input(
        "Donation date (YYYY-MM-DD) [today]: "
    ).strip()

    if donation_date:

        try:

            donation_date = datetime.strptime(
                donation_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            error(
                "Invalid date. Use YYYY-MM-DD."
            )

            return

    else:

        donation_date = None

    result = record_donation(
        donor_id=int(donor_id),
        location_id=int(location_id),
        donation_date=donation_date
    )

    if result.get("success"):

        success(
            result.get(
                "message",
                "Donation recorded successfully."
            )
        )

        print(
            f"Donation ID: "
            f"{result.get('donation_id')}"
        )

    else:

        error(
            result.get(
                "message",
                "Donation failed."
            )
        )


# ============================================================
# Donation History
# ============================================================

def donation_history_menu():

    header("DONATION HISTORY")

    donor_id = input(
        "Donor ID: "
    ).strip()

    if not donor_id.isdigit():

        error("Donor ID must be a number.")
        return

    result = get_donation_history(
        int(donor_id)
    )

    if not result.get("success"):

        error(
            result.get(
                "message",
                "Could not retrieve history."
            )
        )

        return

    history = result.get(
        "data",
        []
    )

    if not history:

        print("\nNo donation history found.")
        return

    for donation in history:

        print("\n" + "-" * 45)

        print(
            f"Donation ID: "
            f"{donation.get('donation_id')}"
        )

        print(
            f"Date: "
            f"{donation.get('donation_date')}"
        )

        print(
            f"Volume: "
            f"{donation.get('volume_ml')} ml"
        )

        print(
            f"Location: "
            f"{donation.get('location_name')}"
        )

        print(
            f"District: "
            f"{donation.get('district')}"
        )

    print("-" * 45)


# ============================================================
# Reports
# ============================================================

def reports_menu():

    header("LIFELINK REPORTS")

    report = generate_dashboard_report()

    if not report:

        error("Unable to generate report.")
        return

    if not report.get("total_donors"):

        error("Unable to generate report.")
        return

    if not report["total_donors"].get("success"):

        error("Unable to generate report.")
        return

    print("\nSYSTEM OVERVIEW")
    print("-" * 45)

    print(
        f"Total registered donors: "
        f"{report['total_donors']['data']}"
    )

    print(
        f"Total donations: "
        f"{report['total_donations']['data']}"
    )

    print(
        f"Available donors: "
        f"{report['available_donors']['data']}"
    )

    print("\nDONORS BY BLOOD TYPE")
    print("-" * 45)

    for item in report["blood_types"]["data"]:

        print(
            f"{item['blood_type']:<10}: "
            f"{item['total']}"
        )

    print("\nDONORS BY DISTRICT")
    print("-" * 45)

    for item in report["districts"]["data"]:

        print(
            f"{item['district']:<20}: "
            f"{item['total']}"
        )

    print("-" * 45)


# ============================================================
# Staff / User Menu
# ============================================================

def staff_menu():

    while True:

        header("STAFF / USER MENU")

        print("1. Search Donor")
        print("0. Back")

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            search_donor_menu()

        elif choice == "0":

            break

        else:

            error("Invalid option.")
            pause()


# ============================================================
# Main Menu
# ============================================================

def main_menu():

    while True:

        header(
            "LIFELINK BLOOD DONATION SYSTEM"
        )

        print("1. Administrator Login")
        print("2. Staff / User")
        print("0. Exit")

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            administrator_login()

        elif choice == "2":

            staff_menu()

        elif choice == "0":

            print(
                "\nThank you for using LifeLink."
            )

            print("Goodbye!")

            break

        else:

            error("Invalid option.")
            pause()


# ============================================================
# Start Program
# ============================================================

if __name__ == "__main__":

    try:

        main_menu()

    except KeyboardInterrupt:

        print("\n")
        print("Program stopped by user.")
        print("Thank you for using LifeLink.")
        print("Goodbye!")