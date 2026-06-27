import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

    IG_USER_ID = os.getenv("IG_USER_ID")
    IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")

    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    TIMEZONE = os.getenv("TIMEZONE", "Europe/Vienna")
    DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

    NOTION_VERSION = "2022-06-28"


def validate_config():
    missing = []

    if not Config.NOTION_TOKEN:
        missing.append("NOTION_TOKEN")

    if not Config.NOTION_DATABASE_ID:
        missing.append("NOTION_DATABASE_ID")

    if not Config.DRY_RUN:
        if not Config.IG_USER_ID:
            missing.append("IG_USER_ID")
        if not Config.IG_ACCESS_TOKEN:
            missing.append("IG_ACCESS_TOKEN")

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")