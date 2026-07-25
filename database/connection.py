"""MySQL connection module for the LifeLink Blood Donation System.

Owned by Member 4 (Database & Donations).

Every other module obtains its database handle from here, so this is the
single place that knows how to reach MySQL. Configuration is read from
environment variables (optionally loaded from a local ``.env`` file), so
no credentials are ever hard-coded or committed. See ``.env.example``.

Public API:
    get_connection()      -> mysql.connector connection to the app schema
    get_db_connection()   -> alias of get_connection() (kept because the
                             donor module imports this name)
    init_database()       -> create the schema from database/schema.sql
"""

import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error

try:
    # python-dotenv is listed in requirements.txt. If it is missing we
    # simply fall back to the real environment variables.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - optional dependency
    pass


# Absolute path to database/schema.sql, resolved relative to this file so
# it works no matter which directory the app is launched from.
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def _config(include_database: bool = True) -> dict:
    """Builds the mysql.connector configuration from the environment.

    Args:
        include_database: When False the ``database`` key is omitted, so
            the connection can be used to create the schema before the
            database itself exists.

    Returns:
        A dict of keyword arguments for ``mysql.connector.connect``.
    """
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
    }
    if include_database:
        config["database"] = os.getenv("DB_NAME", "lifelink")
    return config


def get_connection():
    """Opens a new connection to the LifeLink MySQL database.

    Returns:
        An open ``mysql.connector`` connection object. The caller is
        responsible for closing it (use try/finally or a context helper).

    Raises:
        mysql.connector.Error: If the connection cannot be established.
    """
    try:
        return mysql.connector.connect(**_config())
    except Error as error:
        # Surface a clear message but let callers handle the failure.
        print(f"[database] Could not connect to MySQL: {error}")
        raise


# Backwards-compatible alias: the donor module imports ``get_db_connection``.
# Keeping both names avoids breaking already-written code while the team
# standardises on a single name.
get_db_connection = get_connection


def init_database() -> None:
    """Creates the database and all tables from ``schema.sql``.

    Connects without selecting a database (the script issues its own
    ``CREATE DATABASE`` / ``USE``), then executes every statement in
    ``schema.sql``. Safe to run repeatedly.

    Raises:
        FileNotFoundError: If schema.sql cannot be located.
        mysql.connector.Error: If the schema fails to apply.
    """
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    sql_script = SCHEMA_PATH.read_text(encoding="utf-8")

    connection = mysql.connector.connect(**_config(include_database=False))
    try:
        cursor = connection.cursor()
        for statement in _split_statements(sql_script):
            cursor.execute(statement)
        connection.commit()
        print("[database] Schema applied successfully.")
    finally:
        cursor.close()
        connection.close()


def _split_statements(sql_script: str) -> list:
    """Splits a SQL script into individual executable statements.

    Strips full-line ``--`` comments and blank lines, then separates on
    the semicolon terminator. The LifeLink schema contains no semicolons
    inside statements, so a simple split is safe and avoids depending on
    connector-specific multi-statement support.

    Args:
        sql_script: The raw contents of a .sql file.

    Returns:
        A list of non-empty SQL statements (without trailing semicolons).
    """
    lines = []
    for line in sql_script.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    return [stmt.strip() for stmt in cleaned.split(";") if stmt.strip()]


if __name__ == "__main__":
    # Convenience: `python -m database.connection` builds the schema.
    init_database()
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# you are free to play along it
# use .env to use your own variables
#.env must be in the root of the repo
# .env must be included in .gitignore