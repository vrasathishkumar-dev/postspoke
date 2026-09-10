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


def test_get_next_post_time_negative_interval_raises():
    from datetime import datetime
    with pytest.raises(ValueError):
        get_next_post_time(datetime.now(), -10)


# === NEW TEST: TDD - RED phase ===
def test_get_next_n_post_times_returns_n_times():
    """Test that get_next_n_post_times returns n post times."""
    from postspoke.scheduler import get_next_n_post_times
    start_time = datetime(2026, 9, 10, 10, 0, 0)
    result = get_next_n_post_times(start_time, 30, 3)
    assert len(result) == 3
    assert result[0] == datetime(2026, 9, 10, 10, 30, 0)
    assert result[1] == datetime(2026, 9, 10, 11, 0, 0)
    assert result[2] == datetime(2026, 9, 10, 11, 30, 0)


def test_get_next_n_post_times_zero_returns_empty():
    """Test that n=0 returns empty list."""
    from postspoke.scheduler import get_next_n_post_times
    start_time = datetime(2026, 9, 10, 10, 0, 0)
    result = get_next_n_post_times(start_time, 30, 0)
    assert result == []