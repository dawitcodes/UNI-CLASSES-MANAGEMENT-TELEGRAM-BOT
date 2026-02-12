# school-telegram-bot/app/utils/helpers.py

from datetime import datetime

def format_datetime(date_str, input_format="%Y-%m-%d", output_format="%d %b %Y"):
    """
    Convert date string from one format to another.
    Example: '2026-02-11' → '11 Feb 2026'
    """
    try:
        dt = datetime.strptime(date_str, input_format)
        return dt.strftime(output_format)
    except Exception:
        return date_str

def safe_get(dct, key, default="N/A"):
    """
    Safely get a value from a dictionary
    """
    return dct.get(key, default)
