"""
LifeLink - Blood Donation Management System
Main CLI entry point.
"""
from datetime import datetime
from auth.authentication import login
from donors.donor_service import register_donor
from donations.donation_service import record_donation
from search.search_service import search_by_blood_type, search_by_district, search_by_blood_type_and_district
from reports.report_generator import generate_dashboard_report


# ==========================================
# Login
# ==========================================

def login_menu():
    """
    Handles admin login.
    """

    print("\n=== Login ===")

    username = input("Username: ")
    password = input("Password: ")

    result = login(username,password)
    print(result)



# ==========================================
# Register Donor
# ==========================================

def donor_registration_menu():
    """
    Handles donor registration.
    """

    print("\n=== Register Donor ===")
    full_name = input("Full name: ")
    dob_input = input("Date of birth (YYYY-MM-DD): ")
    try:
        date_of_birth = datetime.strptime(
            dob_input,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        print("Invalid date format.")
        return


    blood_type = input("Blood type: ").upper()
    phone = input("Phone: ")
    email = input("Email: ")


    district = input("District: ")


    donor_data = {
        "full_name": full_name,
        "date_of_birth": date_of_birth,
        "blood_type": blood_type,
        "phone": phone,
        "email": email,
        "district": district,
        "is_available": True
    }

    result = register_donor(donor_data)
    print(result)

# ==========================================
# Record Donation
# ==========================================

def donation_menu():
    """
    Records blood donations.
    """
    print("\n=== Record Donation ===")
    try:
        donor_id = int(input("Donor ID: "))
        location_id = int(input("Location ID: "))

    except ValueError:
        print("IDs must be numbers.")
        return

    result = record_donation(donor_id,location_id)
    print(result)

# ==========================================
# Search Donor
# ==========================================

def search_menu():
    """
    Searches donors.
    """

    print("\n=== Search Donor ===")
    print("1. Search by Blood Type")
    print("2. Search by District")
    print("3. Search by Blood Type + District")


    choice = input("Choice: ")

    if choice == "1":

        blood_type = input("Blood type: ").upper()
        result = search_by_blood_type(blood_type)

    elif choice == "2":

        district = input("District: ")
        result = search_by_district(district)


    elif choice == "3":

        blood_type = input("Blood type: ").upper()
        district = input("District: ")
        result = search_by_blood_type_and_district(blood_type,district)

    else:

        print("Invalid option.")
        return

    print()

    if result["success"]:

        donors = result["data"]


        if not donors:

            print("No donors found.")
            return


        for donor in donors:
            print("----------------")
            print(f"ID: {donor['donor_id']}")
            print(f"Name: {donor['full_name']}")
            print(f"Blood Type: {donor['blood_type']}")
            print(f"District: {donor['district']}")

    else:

        print(result["message"])



# ==========================================
# Reports
# ==========================================

def reports_menu():
    """
    Displays system reports.
    """

    print("\n=== Reports ===")
    report = generate_dashboard_report()
    print(report)



# ==========================================
# Main Menu
# ==========================================

def main_menu():
    """
    Displays the main menu and routes user input.
    """
    while True:

        print()        
        print("=== LifeLink Blood Donation Management System ===")
        print("1. Login")
        print("2. Register Donor")
        print("3. Record Donation")
        print("4. Search Donor")
        print("5. Generate Reports")
        print("0. Exit")


        choice = input("Choose option: ")


        if choice == "1":
            login_menu()

        elif choice == "2":
            donor_registration_menu()

        elif choice == "3":
            donation_menu()

        elif choice == "4":
            search_menu()

        elif choice == "5":
            reports_menu()

        elif choice == "0":
            print("Exiting LifeLink...")
            break

        else:

            print("Invalid option.")



# ==========================================
# Program Entry
# ==========================================

if __name__ == "__main__":

    try:

        main_menu()

    except KeyboardInterrupt:

        print(
            "\nApplication closed."
        )