from datetime import datetime

def validate_datetime(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def validate_phone(phone):
    if phone.startswith('+380') and len(phone) == 13 and phone[1:].isdigit():
        return True
    return False

def validate_price(price):
    try:
        price_value = float(price)
        return price_value > 0
    except (ValueError, TypeError):
        return False