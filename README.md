# LifeLink — Blood Donation Management System

LifeLink is a Python command-line blood donation management system designed to help manage blood donors, donations, donor eligibility, blood-group searches, and reporting.

The system uses Python for application logic and MySQL for persistent data storage.

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Application Workflow](#application-workflow)
- [Main Modules](#main-modules)
- [Eligibility Rule](#eligibility-rule)
- [Reports](#reports)
- [Security](#security)
- [Development Guidelines](#development-guidelines)
- [Git Workflow](#git-workflow)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)
- [Presentation Demo](#presentation-demo)
- [Contributors](#contributors)
- [License](#license)
- [Disclaimer](#disclaimer)

## Project Overview

Blood donation management requires accurate information about donors, blood groups, donation history, and donor availability.

LifeLink provides a centralized command-line system for managing this information.

The application allows administrators to:

1. Authenticate securely.
2. Register donors.
3. View and manage donor information.
4. Search for donors by blood type.
5. Search for donors by district.
6. Search using both blood type and district.
7. Check donor eligibility.
8. Record blood donations.
9. View donation history.
10. Generate reports.

## Objectives

The main objectives of LifeLink are to:

- Improve organization of donor information.
- Make donor searching faster.
- Track donation history.
- Prevent donations from donors who have not completed the required waiting period.
- Provide information about available donors.
- Maintain accurate and persistent records using MySQL.
- Provide a simple command-line interface for administrators.

## Key Features

### 1. Administrator Authentication

Administrators can:

- Register an administrator account.
- Log in securely.
- Log out.
- Use password hashing.
- Maintain an authenticated session.

Passwords are stored as hashes rather than plain text.

### 2. Donor Registration

The system stores donor information including:

- Donor ID
- Full name
- Blood type
- District
- Phone number
- Email
- Date of birth
- Last donation date
- Availability status
- Creation timestamp

### 3. Donor Management

The donor service supports:

- Registering a donor.
- Viewing a donor profile.
- Updating donor information.
- Retrieving all donors.
- Validating donor information.

Age is calculated from the donor's date of birth instead of being stored as a permanent value.

### 4. Donor Search

Donors can be searched by blood type, district, or both blood type and district.

Example search:

- Blood type: O+
- District: Gasabo

### 5. Eligibility Checking

LifeLink applies a 56-day waiting period between whole-blood donations.

A donor is considered eligible when:

- They have never donated before, or
- At least 56 days have passed since their last donation.

### 6. Donation Recording

Administrators can record donations using:

- Donor ID
- Donation date
- Donation volume
- Donation location
- Notes

When a donation is recorded, the donor's latest donation date is updated.

### 7. Donation History

The system can retrieve donation history for a donor.

Donation history can include:

- Donation ID
- Donor
- Blood type
- Donation date
- Donation volume
- Donation location
- Notes

### 8. Reports

LifeLink provides five main report categories:

1. Blood Group Distribution
2. Eligible Donors
3. Donation History
4. Donation Activity
5. Emergency Donor Availability

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Application programming language |
| MySQL | Database management |
| mysql-connector-python | Python–MySQL communication |
| bcrypt | Password hashing |
| python-dotenv | Environment variables |
| Git | Version control |
| GitHub | Collaboration |
| VS Code | Development environment |
| CLI | User interface |

## System Architecture

LifeLink follows a modular architecture.

    USER
      |
      v
    main.py
      |
      +----------------+----------------+
      |                |                |
      v                v                v
    AUTH             DONORS          SEARCH
      |                |                |
      +----------------+----------------+
                       |
                       v
                   DONATIONS
                       |
                       v
                    REPORTS
                       |
                       v
              DATABASE CONNECTION
                       |
                       v
                     MySQL

Each module has a specific responsibility.

### main.py

Acts as the entry point and CLI controller.

### auth/

Handles administrator authentication.

### donors/

Handles donor information and management.

### search/

Handles donor searching and eligibility.

### donations/

Handles donation records and history.

### reports/

Generates reports from the database.

### database/

Contains the database connection and SQL schema.

## Project Structure

    LifeLink/
    │
    ├── main.py
    ├── README.md
    ├── requirements.txt
    ├── .env
    ├── .gitignore
    │
    ├── auth/
    │   ├── __init__.py
    │   └── authentication.py
    │
    ├── database/
    │   ├── __init__.py
    │   ├── connection.py
    │   └── schema.sql
    │
    ├── donors/
    │   ├── __init__.py
    │   ├── donors.py
    │   └── donor_service.py
    │
    ├── search/
    │   ├── __init__.py
    │   ├── search_service.py
    │   └── eligibility_checker.py
    │
    ├── donations/
    │   ├── __init__.py
    │   └── donation_service.py
    │
    └── reports/
        ├── __init__.py
        └── report_generator.py

## Database Design

LifeLink uses four main database tables:

    administrators
          |
          | authentication
          |
          v
        donors
          |
          | donor_id
          v
      donations
          |
          | location_id
          v
    donation_locations

### Administrators

Stores administrator accounts.

Important fields include:

- admin_id
- username
- password_hash
- created_at

### Donors

Stores donor information.

Important fields include:

- donor_id
- full_name
- blood_type
- district
- phone
- email
- date_of_birth
- last_donation_date
- is_available
- created_at

Valid blood types are:

- A+
- A-
- B+
- B-
- AB+
- AB-
- O+
- O-

### Donation Locations

Stores locations where donations take place.

Important fields include:

- location_id
- location_name
- district

### Donations

Stores individual donation records.

Important fields include:

- donation_id
- donor_id
- location_id
- donation_date
- volume_ml

Foreign keys connect donations to donors and donation locations.

## Installation

### Requirements

Before installing LifeLink, make sure you have:

- Python 3
- MySQL or MariaDB
- Git
- VS Code or another code editor
- Terminal

Check Python:

    python3 --version

Check MySQL:

    mysql --version

### Clone the Repository

    git clone <YOUR_REPOSITORY_URL>

Enter the project directory:

    cd lifelink-blood-donation-system

### Create a Virtual Environment

    python3 -m venv .venv

Activate it on Linux or macOS:

    source .venv/bin/activate

On Windows:

    .venv\Scripts\activate

### Install Dependencies

    pip install -r requirements.txt

The project dependencies include:

    mysql-connector-python
    bcrypt
    python-dotenv

## Environment Variables

Create a .env file in the project root.

Example:

    DB_HOST=your_database_host
    DB_PORT=3306
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_NAME=lifelink

For a local MySQL database:

    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=lifelink

Never commit your real .env file to GitHub.

Add the following to .gitignore:

    .env
    .venv/
    __pycache__/
    *.pyc

## Database Setup

The database schema is located at:

    database/schema.sql

Run:

    mysql -u root -p < database/schema.sql

Or enter MySQL:

    mysql -u root -p

Then run:

    SOURCE database/schema.sql;

## Running the Application

From the project root:

    python3 main.py

The CLI will provide options similar to:

    ========================================
         LIFELINK BLOOD DONATION SYSTEM
    ========================================

    1. Login
    2. Register Donor
    3. Record Donation
    4. Search Donor
    5. Check Eligibility
    6. Donation History
    7. Generate Reports
    0. Exit

    Choose an option:

## Application Workflow

    Start
      |
      v
    Login
      |
      v
    Authentication successful?
      |
      +---- No ----> Try again / Exit
      |
     Yes
      |
      v
    Main Menu
      |
      +----> Register Donor
      |
      +----> Search Donor
      |
      +----> Check Eligibility
      |
      +----> Record Donation
      |
      +----> Donation History
      |
      +----> Generate Reports
      |
      +----> Logout
      |
      v
    Exit

## Main Modules

### database/connection.py

Responsible for creating MySQL connections.

Other modules use the database connection function to communicate with MySQL.

### database/schema.sql

Defines the database structure and relationships.

### auth/authentication.py

Responsible for:

- Password hashing
- Password verification
- Administrator registration
- Administrator login
- Logout

### donors/donors.py

Contains the Donor data model.

### donors/donor_service.py

Responsible for:

- Registering donors
- Validating donor information
- Viewing donors
- Updating donors
- Retrieving donor records

### search/search_service.py

Responsible for donor searches by:

- Blood type
- District
- Blood type and district
- Donor ID

### search/eligibility_checker.py

Determines whether a donor has completed the required waiting period.

### donations/donation_service.py

Responsible for:

- Recording donations
- Validating donors
- Checking eligibility
- Updating donation dates
- Retrieving donation history

### reports/report_generator.py

Generates the project's reports.

### main.py

The main CLI entry point.

It coordinates the different modules and handles user interaction.

## Eligibility Rule

LifeLink uses a 56-day waiting period between donations.

The logic is:

    Has donor donated before?
           |
           +---- No ----> Eligible
           |
          Yes
           |
           v
    Calculate days since last donation
           |
           v
       Is days >= 56?
           |
       +---+---+
       |       |
      Yes      No
       |       |
       v       v
    Eligible  Not Eligible

## Reports

### 1. Blood Group Distribution

Shows the number of donors in each blood group.

Example:

    Blood Type    Donors
    --------------------
    A+            10
    A-             4
    B+             8
    O+            15
    O-             6

### 2. Eligible Donors

Lists donors who currently satisfy the eligibility requirement.

### 3. Donation History

Displays donation records for donors.

### 4. Donation Activity

Shows donation activity grouped by time period.

### 5. Emergency Donor Availability

Shows available donors who can potentially be contacted during emergency situations.

## Security

LifeLink uses several basic security practices.

### Password Hashing

Administrator passwords are hashed instead of stored as plain text.

### Environment Variables

Database credentials should be stored in .env.

### Parameterized SQL

SQL queries use parameters instead of directly inserting user input into SQL statements.

This helps protect against SQL injection.

### Database Constraints

The database uses:

- Primary keys
- Foreign keys
- Unique constraints
- NOT NULL constraints
- Valid blood-type constraints
- Indexes

## Development Guidelines

When contributing to LifeLink:

1. Create a branch for your feature.
2. Keep commits focused.
3. Never commit .env.
4. Use meaningful function names.
5. Keep modules focused on one responsibility.
6. Use parameterized SQL queries.
7. Test changes before creating a pull request.
8. Keep database and Python field names consistent.
9. Update documentation when functionality changes.

## Git Workflow

Create a feature branch:

    git checkout -b feature/your-feature

Check your changes:

    git status

Stage your changes:

    git add .

Commit:

    git commit -m "Add donor search functionality"

Push your branch:

    git push origin feature/your-feature

Then create a Pull Request.

## Testing

Test the database connection.

    python3 database/connection.py

Test authentication:

- Administrator registration
- Correct login
- Incorrect password
- Unknown username
- Logout

Test donors:

- Valid donor registration
- Invalid blood type
- Invalid phone
- Invalid email
- Invalid date of birth
- Viewing donor
- Updating donor

Test search:

- Search by blood type
- Search by district
- Search by blood type and district
- Search with no matching results

Test eligibility:

- Donor has never donated
- Donation less than 56 days ago
- Donation exactly 56 days ago
- Donation more than 56 days ago

Test donations:

- Valid donation
- Unknown donor
- Invalid location
- Ineligible donor
- Donation history

Test reports:

1. Blood Group Distribution
2. Eligible Donors
3. Donation History
4. Donation Activity
5. Emergency Donor Availability

## Troubleshooting

### ModuleNotFoundError

Run the project from the root directory:

    cd lifelink-blood-donation-system
    python3 main.py

### MySQL Connection Error

Check the following values in your .env file:

- DB_HOST
- DB_PORT
- DB_USER
- DB_PASSWORD
- DB_NAME

Also make sure MySQL is running.

### Database Does Not Exist

Run:

    mysql -u root -p < database/schema.sql

### Missing Python Package

Activate your virtual environment:

    source .venv/bin/activate

Then install the dependencies:

    pip install -r requirements.txt

## Future Improvements

Future versions of LifeLink could include:

- Web interface
- Graphical user interface
- SMS notifications
- Email notifications
- Blood-stock inventory tracking
- Hospital accounts
- Blood-bank accounts
- Role-based permissions
- Automated donor reminders
- Advanced analytics
- CSV/PDF report exports
- Automated tests with pytest
- Audit logs
- Cloud deployment

## Learning Outcomes

Through LifeLink, developers gain practical experience with:

- Python
- Object-Oriented Programming
- Dataclasses
- Functions
- Modules
- Exception handling
- Input validation
- MySQL
- SQL
- SQL JOINs
- Primary keys
- Foreign keys
- Database transactions
- Password hashing
- Environment variables
- Git
- GitHub
- CLI development
- Modular architecture

## Presentation Demo

A simple presentation demonstration can follow this workflow:

    1. Start LifeLink
            |
            v
    2. Login as Administrator
            |
            v
    3. Register a Donor
            |
            v
    4. Search for the Donor
            |
            v
    5. Check Eligibility
            |
            v
    6. Record a Donation
            |
            v
    7. View Donation History
            |
            v
    8. Generate Reports
            |
            v
    9. Logout

## Contributors

LifeLink was developed as a collaborative project.

| Role | Contributor |
|---|---|
| Project Manager & System Integration | Member 1 |
| Authentication & Administration | Member 2 |
| Donor Registration & Management | Member 3 |
| Database & Donations | Member 4 |
| Search & Eligibility | Member 5 |
| Additional Module | Member 6 |

Replace the placeholder contributor names with the actual team members before submitting the project.

## License

This project was developed as an academic/team software project.

## Disclaimer

LifeLink is an educational software project designed to demonstrate blood donation management concepts.

The 56-day eligibility rule implemented by this application is a project requirement and should not be considered medical advice. Actual blood donation eligibility should be determined by qualified healthcare professionals and applicable medical guidelines.
