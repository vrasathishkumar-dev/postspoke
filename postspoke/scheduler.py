from datetime import timedelta

def get_next_post_time(start_time, interval_minutes):
    """Calculate the next post time given a start time and interval in minutes."""
    return start_time + timedelta(minutes=interval_minutes)