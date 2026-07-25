#!/usr/bin/env bash
# =====================================================================
# LifeLink - MySQL backup & recovery helper
# Owner: Member 4 (Database & Donations)
# Covers the guide's "database backup and recovery considerations".
#
# Reads DB credentials from the repo-root .env file (same file the app
# uses), so it never hard-codes passwords.
#
# Usage:
#   ./database/backup.sh backup            # dump to backups/lifelink_<timestamp>.sql
#   ./database/backup.sh restore <file>    # restore a dump into the database
#
# Requires the mysql client tools (mysqldump, mysql) on PATH.
# =====================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${REPO_ROOT}/.env"
BACKUP_DIR="${REPO_ROOT}/backups"

# Load .env (KEY=VALUE lines) into the environment.
if [[ -f "${ENV_FILE}" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "${ENV_FILE}"
    set +a
else
    echo "Error: ${ENV_FILE} not found. Copy .env.example to .env first." >&2
    exit 1
fi

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_NAME="${DB_NAME:-lifelink}"

do_backup() {
    mkdir -p "${BACKUP_DIR}"
    local stamp
    stamp="$(date +%Y%m%d_%H%M%S)"
    local outfile="${BACKUP_DIR}/lifelink_${stamp}.sql"
    mysqldump \
        --host="${DB_HOST}" --port="${DB_PORT}" \
        --user="${DB_USER}" --password="${DB_PASSWORD}" \
        --single-transaction --routines --triggers \
        "${DB_NAME}" > "${outfile}"
    echo "Backup written to ${outfile}"
}

do_restore() {
    local infile="${1:-}"
    if [[ -z "${infile}" || ! -f "${infile}" ]]; then
        echo "Error: provide an existing dump file to restore." >&2
        echo "Usage: $0 restore <file.sql>" >&2
        exit 1
    fi
    mysql \
        --host="${DB_HOST}" --port="${DB_PORT}" \
        --user="${DB_USER}" --password="${DB_PASSWORD}" \
        "${DB_NAME}" < "${infile}"
    echo "Restored ${infile} into database '${DB_NAME}'"
}

case "${1:-}" in
    backup)  do_backup ;;
    restore) do_restore "${2:-}" ;;
    *)
        echo "Usage: $0 {backup|restore <file>}" >&2
        exit 1
        ;;
esac
