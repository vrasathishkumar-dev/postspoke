from datetime import datetime, timedelta

def get_next_post_time(start_time, interval_minutes):
    """Get the next post time after start_time by adding interval_minutes.

    Args:
        start_time (datetime): The starting timestamp
        interval_minutes (int): Minutes to add (must be non-negative)

    Returns:
        datetime: The next post time

    Raises:
        ValueError: If interval_minutes is negative
    """
    if interval_minutes < 0:
        raise ValueError("interval_minutes must be non-negative")
    return start_time + timedelta(minutes=interval_minutes)

def get_next_n_post_times(start_time, interval_minutes, n):
    """Get n post times starting from start_time with given interval.

    Args:
        start_time (datetime): The starting timestamp
        interval_minutes (int): Minutes between posts (must be non-negative)
        n (int): Number of post times to generate (must be non-negative)

    Returns:
        list[datetime]: List of n post times

    Raises:
        ValueError: If interval_minutes or n is negative
    """
    if interval_minutes < 0:
        raise ValueError("interval_minutes must be non-negative")
    if n < 0:
        raise ValueError("n must be non-negative")
    return [start_time + timedelta(minutes=interval_minutes * (i + 1)) for i in range(n)]
