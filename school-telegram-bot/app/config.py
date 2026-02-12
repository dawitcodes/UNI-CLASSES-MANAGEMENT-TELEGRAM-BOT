import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# List of admin Telegram user IDs (class reps)
ADMIN_IDS = [123456789]  # replace with real IDs
