from datetime import datetime

def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def format_date_for_display(date_str: str) -> str:
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")