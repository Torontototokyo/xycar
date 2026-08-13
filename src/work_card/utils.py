import re
def chinese_duration_to_hours(text: str) -> float:
    """Convert '2天3小时15分30秒' → total hours (float)"""
    if not isinstance(text, str) or not text.strip():
        return 0.0
    
    text = text.strip()
    
    days    = re.search(r'(\d+)\s*天', text)
    hours   = re.search(r'(\d+)\s*小时', text)
    minutes = re.search(r'(\d+)\s*分', text)
    seconds = re.search(r'(\d+)\s*秒', text)
    
    total = 0.0
    if days:    total += int(days.group(1)) * 24
    if hours:   total += int(hours.group(1))
    if minutes: total += int(minutes.group(1)) / 60.0
    # if seconds: total += int(seconds.group(1)) / 3600.0
    
    return round(total, 2)   # Change to 2 if you prefer

