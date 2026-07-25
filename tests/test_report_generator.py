"""Unit tests for auth/authentication.py. Owned by Member 6."""

from unittest.mock import MagicMock, patch
from auth import authentication


def test_hash_password_and_verify_roundtrip():
    plain = "correct-horse-battery-staple"
    hashed = authentication.hash_password(plain)
    assert hashed != plain
    assert authentication.verify_password(plain, hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = authentication.hash_password("real-password")
    assert authentication.verify_password("wrong-password", hashed) is False


def test_validate_login_input_requires_identifier():
    error = authentication._validate_login_input("", "somepassword")
    assert error is not None


def test_validate_login_input_requires_password():
    error = authentication._validate_login_input("admin@example.com", "")
    assert error is not None


@patch("auth.authentication.get_connection")
def test_login_rejects_unknown_identifier(mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    result = authentication.login("nobody@example.com", "whatever")
    assert result["success"] is False


def test_logout_returns_false_for_unknown_session():
    assert authentication.logout("nonexistent-session-id") is False