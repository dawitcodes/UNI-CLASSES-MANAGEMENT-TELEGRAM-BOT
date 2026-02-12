# Replace with real Telegram user IDs
ADMIN_IDS = {
    6775548145,  # example admin ID
}

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
