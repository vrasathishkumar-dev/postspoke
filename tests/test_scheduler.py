import pytest
from datetime import datetime, timedelta
from postspoke.scheduler import get_next_post_time


def test_get_next_post_time_basic():
    """Test that given a start time and interval, returns the next time."""
    start_time = datetime(2026, 9, 10, 10, 0, 0)
    interval_minutes = 30
    expected = datetime(2026, 9, 10, 10, 30, 0)
    result = get_next_post_time(start_time, interval_minutes)
    assert result == expected


def test_get_next_post_time_wraps_hour():
    """Test that interval wraps correctly across hours."""
    start_time = datetime(2026, 9, 10, 10, 45, 0)
    interval_minutes = 30
    expected = datetime(2026, 9, 10, 11, 15, 0)
    result = get_next_post_time(start_time, interval_minutes)
    assert result == expected
