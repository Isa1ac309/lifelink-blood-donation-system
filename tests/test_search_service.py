"""Unit tests for search/search_service.py. Owned by Member 6."""

from unittest.mock import MagicMock, patch
from search import search_service


def test_search_by_blood_type_returns_empty_for_blank_input():
    assert search_service.search_by_blood_type("") == []


def test_search_by_district_returns_empty_for_blank_input():
    assert search_service.search_by_district("") == []


@patch("search.search_service.get_db_connection")
def test_search_by_blood_type_uppercases_input(mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    search_service.search_by_blood_type("o+")
    called_args = mock_cursor.execute.call_args[0]
    assert called_args[1] == ("O+",)


@patch("search.search_service.get_db_connection")
def test_combined_search_requires_both_fields(mock_get_conn):
    result = search_service.search_by_blood_type_and_district("O+", "")
    assert result == []