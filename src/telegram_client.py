import requests


class TelegramClient:
    BASE_URL = "https://api.telegram.org"

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send(self, message: str):
        """Send a text message to the configured chat."""
        url = f"{self.BASE_URL}/bot{self.bot_token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()

            if not data.get("ok"):
                print(f"  Telegram error: {data}")
            else:
                print(f"  Telegram notification sent.")

        except Exception as e:
            # Telegram errors should never crash the main script
            print(f"  Telegram notification failed: {e}")
