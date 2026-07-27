"""
LifeLink Blood Donation Management System
Main CLI Application
"""

from datetime import datetime

from auth.authentication import login, register_admin

from donors.donor_service import register_donor ,get_donor_by_id, get_donor_by_name

from donations.donation_service import record_donation,  get_donation_history

from reports.report_generator import generate_dashboard_report


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

    result = login(username, password)

    if result.get("success"):

        success("Login successful.")

        admin = result.get("admin")

        if admin:
            administrator_menu(admin)

    else:
        error(result.get("message", "Login failed."))


# ============================================================
# Register New Administrator
# ============================================================

def register_new_administrator():

    header("REGISTER NEW ADMINISTRATOR")

    username = input("Username: ").strip()
    password = input("Password: ")

    if not username or not password:
        error("Username and password cannot be empty.")
        return

    result = register_admin(username, password)

    if result.get("success"):
        success("Administrator registered successfully.")
    else:
        error(result.get("message", "Registration failed."))


# ============================================================
# Administrator Menu
# ============================================================

def administrator_menu(admin):

    while True:

        header("ADMINISTRATOR MENU")

        print(f"Logged in as: {admin.get('username')}")
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
            pause()

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

    blood_type = input("Blood type: ").strip().upper()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    district = input("District: ").strip()

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
            f"Donor ID: {result.get('donor_id')}"
        )

    else:

        error(
            result.get(
                "message",
                "Donor registration failed."
            )
        )


# ============================================================
# Display Donor
# ============================================================

def display_donor(donor):

    print("\n" + "-" * 45)

    print(f"ID:            {donor.get('donor_id')}")
    print(f"Name:          {donor.get('full_name')}")
    print(f"Blood Type:    {donor.get('blood_type')}")
    print(f"Phone:         {donor.get('phone')}")
    print(f"Email:         {donor.get('email')}")
    print(f"District:      {donor.get('district')}")

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
# Search Donor
# ============================================================

def search_donor_menu():

    header("SEARCH DONOR")

    print("1. Search by Donor ID")
    print("2. Search by Name")
    print("0. Back")

    choice = input("\nChoose option: ").strip()

    if choice == "1":

        search_donor_by_id()

    elif choice == "2":

        search_donor_by_name()

    elif choice == "0":

        return

    else:

        error("Invalid option.")


# ============================================================
# Search Donor By ID
# ============================================================

def search_donor_by_id():

    donor_id = input("Enter Donor ID: ").strip()

    if not donor_id.isdigit():

        error("Donor ID must be a number.")
        return

    result = get_donor_by_id(
        int(donor_id)
    )

    if result.get("success"):

        display_donor(result["data"])

    else:

        error(
            result.get(
                "message",
                "Donor not found."
            )
        )


# ============================================================
# Search Donor By Name
# ============================================================

def search_donor_by_name():

    name = input("Enter donor name: ").strip()

    if not name:

        error("Name cannot be empty.")
        return

    result = get_donor_by_name(name)

    if result.get("success"):

        display_donor(result["data"])
        return

    if result.get("data"):

        print("\nMultiple donors found:")

        for donor in result["data"]:

            print(
                f"ID: {donor['donor_id']} | "
                f"Name: {donor['full_name']} | "
                f"Blood: {donor['blood_type']} | "
                f"District: {donor['district']}"
            )

    else:

        error(
            result.get(
                "message",
                "Donor not found."
            )
        )


# ============================================================
# Record Donation
# ============================================================

def record_donation_menu():

    header("RECORD DONATION")

    donor_id = input("Donor ID: ").strip()

    if not donor_id.isdigit():

        error("Donor ID must be a number.")
        return

    location_id = input("Location ID: ").strip()

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

            error("Invalid date. Use YYYY-MM-DD.")
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

    donor_id = input("Donor ID: ").strip()

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
                "Could not retrieve donation history."
            )
        )

        return

    history = result.get("data", [])

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
# Staff/User Menu
# ============================================================

def staff_menu():

    while True:

        header("STAFF/USER MENU")

        print("1. Search Donor")
        print("2. Check Eligibility")
        print("3. View Available Blood")
        print("0. Exit")

        choice = input("\nChoose option: ").strip()

        if choice == "1":

            search_donor_menu()
            pause()

        elif choice == "2":

            print(
                "\nEligibility checker will be connected here."
            )
            pause()

        elif choice == "3":

            print(
                "\nBlood availability will be connected here."
            )
            pause()

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

        header("LIFELINK BLOOD DONATION SYSTEM")

        print("1. Administrator Login")
        print("2. Staff/User")
        print("0. Exit")

        choice = input("\nChoose option: ").strip()

        if choice == "1":

            administrator_login()

        elif choice == "2":

            staff_menu()

        elif choice == "0":

            print("\nThank you for using LifeLink.")
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