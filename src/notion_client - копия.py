import requests


class NotionClient:
    def __init__(self, token: str, database_id: str, notion_version: str):
        self.token = token
        self.database_id = database_id
        self.notion_version = notion_version

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json",
        }

    def find_ready_post_by_date(self, publish_date: str):
        """
        Finds one post where:
        - Publish Date = publish_date
        - Status = ready
        """

        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        payload = {
            "filter": {
                "and": [
                    {
                        "property": "Publish Date",
                        "date": {
                            "equals": publish_date
                        }
                    },
                    {
                        "property": "Status",
                        "select": {
                            "equals": "ready"
                        }
                    }
                ]
            },
            "sorts": [
                {
                    "property": "Day",
                    "direction": "ascending"
                }
            ],
            "page_size": 1
        }

        response = requests.post(url, headers=self.headers, json=payload, timeout=30)

        if response.status_code != 200:
            raise RuntimeError(
                f"Notion API error {response.status_code}: {response.text}"
            )

        data = response.json()
        results = data.get("results", [])

        if not results:
            return None

        return self._parse_post(results[0])

    def _parse_post(self, page: dict):
        properties = page.get("properties", {})

        return {
            "page_id": page.get("id"),
            "title": self._get_text(properties, "Title"),
            "day": self._get_number(properties, "Day"),
            "publish_date": self._get_date(properties, "Publish Date"),
            "category": self._get_select(properties, "Category"),
            "caption": self._get_text(properties, "Caption"),
            "hashtags": self._get_text(properties, "Hashtags"),
            "image_url": self._get_url(properties, "Image URL"),
            "status": self._get_select(properties, "Status"),
            "ig_post_id": self._get_text(properties, "IG Post ID"),
        }

    def _get_title(self, properties: dict, name: str) -> str:
        items = properties.get(name, {}).get("title", [])
        return "".join(item.get("plain_text", "") for item in items).strip()

    def _get_text(self, properties: dict, name: str) -> str:
        items = properties.get(name, {}).get("rich_text", [])
        return "".join(item.get("plain_text", "") for item in items).strip()

    def _get_number(self, properties: dict, name: str):
        return properties.get(name, {}).get("number")

    def _get_select(self, properties: dict, name: str) -> str:
        select = properties.get(name, {}).get("select")
        return select.get("name") if select else ""

    def _get_date(self, properties: dict, name: str) -> str:
        date_obj = properties.get(name, {}).get("date")
        return date_obj.get("start") if date_obj else ""

    def _get_url(self, properties: dict, name: str) -> str:
        return properties.get(name, {}).get("url") or ""
