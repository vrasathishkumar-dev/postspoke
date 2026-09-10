from datetime import datetime, timedelta

def get_next_post_time(start_time, interval_minutes):
    if interval_minutes < 0:
        raise ValueError("interval_minutes must be non-negative")
    return start_time + timedelta(minutes=interval_minutes)

def get_next_n_post_times(start_time, interval_minutes, n):
    if interval_minutes < 0:
        raise ValueError("interval_minutes must be non-negative")
    return [start_time + timedelta(minutes=interval_minutes * (i + 1)) for i in range(n)]
