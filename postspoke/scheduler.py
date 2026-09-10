from datetime import timedelta

def get_next_post_time(start_time, interval_minutes):
    if interval_minutes < 0:
        raise ValueError("interval_minutes must be non-negative")
    return start_time + timedelta(minutes=interval_minutes)