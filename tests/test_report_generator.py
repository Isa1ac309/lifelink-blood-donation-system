"""Unit tests for reports/report_generator.py. Owned by Member 6."""

from unittest.mock import MagicMock, patch
from reports import report_generator


@patch("reports.report_generator.get_connection")
def test_blood_group_distribution_returns_rows(mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"blood_type": "O+", "donor_count": 12},
        {"blood_type": "A-", "donor_count": 3},
    ]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    result = report_generator.blood_group_distribution()
    assert result["success"] is True
    assert result["data"] == [
        {"blood_type": "O+", "donor_count": 12},
        {"blood_type": "A-", "donor_count": 3},
    ]


@patch("reports.report_generator.get_connection")
def test_eligible_donors_returns_empty_on_no_match(mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    result = report_generator.eligible_donors()
    assert result["success"] is True
    assert result["data"] == []


def test_render_report_handles_failure():
    result = {"success": False, "message": "connection lost"}
    output = report_generator.render_report("Test Report", result)
    assert "connection lost" in output


def test_render_report_handles_empty_data():
    result = {"success": True, "data": []}
    output = report_generator.render_report("Test Report", result)
    assert "(no data)" in output