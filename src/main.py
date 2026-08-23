from datetime import datetime, timezone

import pytz
import requests

from config import Config, validate_config
from notion_client import NotionClient
from instagram_client import InstagramClient
from telegram_client import TelegramClient

# Token expiry as Unix timestamp - update this when you refresh the token
IG_TOKEN_EXPIRES_AT = 1787670428

TOKEN_WARNING_DAYS = 14  # Warn this many days before expiry


def check_token_expiry(telegram: "TelegramClient | None"):
    """Warn via Telegram if the token is expiring soon."""
    now = datetime.now(timezone.utc).timestamp()
    days_left = (IG_TOKEN_EXPIRES_AT - now) / 86400

    if days_left < 0:
        msg = "🔴 Instagram access token has EXPIRED. Please renew it immediately."
        print(msg)
        if telegram:
            telegram.send(msg)
    elif days_left <= TOKEN_WARNING_DAYS:
        msg = f"⚠️ Instagram access token expires in {int(days_left)} days. Please renew it soon."
        print(msg)
        if telegram:
            telegram.send(msg)
    else:
        print(f"  Token valid for {int(days_left)} more days.")


def validate_image_url(image_url: str):
    if not image_url:
        raise RuntimeError("Image URL is empty")

    if not image_url.startswith("http://") and not image_url.startswith("https://"):
        raise RuntimeError("Image URL must start with http:// or https://")

    response = requests.head(image_url, timeout=15, allow_redirects=True)

    if response.status_code >= 400:
        raise RuntimeError(f"Image URL is not reachable: HTTP {response.status_code}")

    content_type = response.headers.get("Content-Type", "")

    if not content_type.startswith("image/"):
        raise RuntimeError(f"URL does not look like an image. Content-Type: {content_type}")


def get_today_date() -> str:
    timezone = pytz.timezone(Config.TIMEZONE)
    return datetime.now(timezone).date().isoformat()

DEFAULT_HASHTAGS = "#VictoriaOfTheDay #Victoria"


def build_caption(post: dict) -> str:
    caption = post.get("caption", "").strip()
    hashtags = post.get("hashtags", "").strip()

    if caption and hashtags:
        return f"{caption}\n\n{hashtags}"

    return caption or hashtags


def get_telegram() -> "TelegramClient | None":
    if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
        return TelegramClient(
            bot_token=Config.TELEGRAM_BOT_TOKEN,
            chat_id=Config.TELEGRAM_CHAT_ID,
        )
    return None


def main():
    validate_config()

    today = get_today_date()
    telegram = get_telegram()

    # Check token expiry every day
    check_token_expiry(telegram)

    notion = NotionClient(
        token=Config.NOTION_TOKEN,
        database_id=Config.NOTION_DATABASE_ID,
        notion_version=Config.NOTION_VERSION,
    )

    print(f"Looking for Ready post for date: {today}")

    post = notion.find_ready_post_by_date(today)

    if not post:
        msg = f"⚠️ No ready post found for {today}."
        print(msg)
        if telegram:
            telegram.send(msg)
        return

    if post.get("ig_post_id"):
        msg = f"⚠️ Post already published (IG Post ID: {post['ig_post_id']}). Skipping."
        print(msg)
        if telegram:
            telegram.send(msg)
        return

    print("Ready post found:")
    print(f"  Day:      {post['day']}")
    print(f"  Title:    {post['title']}")
    print(f"  Category: {post['category']}")
    print(f"  Image URL:{post['image_url']}")

    try:
        validate_image_url(post["image_url"])
        print("  Image URL validation: OK")
    except RuntimeError as e:
        msg = f"❌ Error: Day {post['day']} — {post['title']}\n{e}"
        print(msg)
        notion.mark_as_error(post["page_id"], str(e))
        if telegram:
            telegram.send(msg)
        return

    final_caption = build_caption(post)
    print("Final caption:")
    print(final_caption)

    if Config.DRY_RUN:
        msg = f"🧪 DRY RUN: Day {post['day']} — {post['title']}\nWould publish but DRY_RUN=true."
        print(msg)
        if telegram:
            telegram.send(msg)
        return

    instagram = InstagramClient(
        ig_user_id=Config.IG_USER_ID,
        access_token=Config.IG_ACCESS_TOKEN,
    )

    try:
        print("\nPublishing to Instagram...")
        ig_post_id = instagram.publish(post["image_url"], final_caption)

        notion.mark_as_posted(post["page_id"], ig_post_id)
        print("Notion status → posted")

        msg = f"✅ Posted: Day {post['day']} — {post['title']}"
        print(msg)
        if telegram:
            telegram.send(msg)

    except Exception as error:
        notion.mark_as_error(post["page_id"], str(error))

        msg = f"❌ Error: Day {post['day']} — {post['title']}\n{error}"
        print(msg)
        if telegram:
            telegram.send(msg)


if __name__ == "__main__":
    main()