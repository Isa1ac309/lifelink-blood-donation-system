"""
main.py

LifeLink - Blood Donation Management System
Main CLI entry point.
"""


def safe_import(module_path, names):
    """Try to import functions from a module; return None for any that fail."""
    result = {}
    try:
        module = __import__(module_path, fromlist=names)
        for name in names:
            result[name] = getattr(module, name, None)
    except ImportError:
        for name in names:
            result[name] = None
    return result


auth = safe_import("auth.authentication", ["login", "logout", "register_admin"])
donors = safe_import("donors.donor_service", ["register_donor", "view_donor_profile", "update_donor_profile"])
donations = safe_import("donations.donation_service", ["record_donation", "view_donation_history"])
search = safe_import("search.search_service", ["search_by_blood_type", "search_by_district"])
reports = safe_import("reports.report_generator", ["generate_summary_report"])

current_session = {"session_id": None, "admin_id": None}


def handle_login():
    identifier = input("Email or phone: ")
    password = input("Password: ")
    if auth["login"] is None:
        print("Login is not available yet.")
        return
    result = auth["login"](identifier, password)
    if result.get("success"):
        current_session["session_id"] = result["session_id"]
        current_session["admin_id"] = result["admin_id"]
        print("Login successful.")
    else:
        print("Login failed: {}".format(result.get("error")))


def handle_register_donor():
    if donors["register_donor"] is None:
        print("Donor registration is not available yet.")
        return
    full_name = input("Full name: ")
    blood_type = input("Blood type: ")
    phone = input("Phone: ")
    district = input("District: ")
    result = donors["register_donor"](full_name, blood_type, phone, district)
    print(result)


def handle_record_donation():
    if donations["record_donation"] is None:
        print("Recording donations is not available yet.")
        return
    donor_id = input("Donor ID: ")
    center = input("Donation center: ")
    result = donations["record_donation"](donor_id, center)
    print(result)


def handle_search_donor():
    if search["search_by_blood_type"] is None:
        print("Search is not available yet.")
        return
    print("1. Search by blood type")
    print("2. Search by district")
    choice = input("Choose: ")
    if choice == "1":
        blood_type = input("Blood type: ")
        results = search["search_by_blood_type"](blood_type)
    else:
        district = input("District: ")
        results = search["search_by_district"](district)

    if not results:
        print("No matching donors found.")
    else:
        for donor in results:
            print(donor)


def handle_reports():
    if reports["generate_summary_report"] is None:
        print("Reports are not available yet.")
        return
    print(reports["generate_summary_report"]())


def main_menu():
    """Displays the main menu and routes user input."""
    while True:
        print("\n=== LifeLink Blood Donation Management System ===")
        print("1. Login")
        print("2. Register Donor")
        print("3. Record Donation")
        print("4. Search Donor")
        print("5. Generate Reports")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            handle_login()
        elif choice == "2":
            handle_register_donor()
        elif choice == "3":
            handle_record_donation()
        elif choice == "4":
            handle_search_donor()
        elif choice == "5":
            handle_reports()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main_menu()