from datetime import datetime

def get_time():
    return datetime.now().strftime("%H:%M:%S")


def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))
