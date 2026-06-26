import time
import requests


class InstagramClient:
    BASE_URL = "https://graph.facebook.com/v19.0"

    def __init__(self, ig_user_id: str, access_token: str):
        self.ig_user_id = ig_user_id
        self.access_token = access_token

    def create_media_container(self, image_url: str, caption: str) -> str:
        """
        Step 1: Upload the image and caption to Instagram.
        Returns a container ID.
        """
        url = f"{self.BASE_URL}/{self.ig_user_id}/media"

        payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token,
        }

        response = requests.post(url, data=payload, timeout=30)
        data = response.json()

        if "error" in data:
            raise RuntimeError(
                f"Instagram create container error: {data['error']['message']}"
            )

        container_id = data.get("id")

        if not container_id:
            raise RuntimeError("Instagram did not return a container ID.")

        print(f"  Media container created: {container_id}")
        return container_id

    def wait_for_container(self, container_id: str, max_attempts: int = 10):
        """
        Instagram needs a moment to process the image before publishing.
        Polls the container status until it is ready.
        """
        url = f"{self.BASE_URL}/{container_id}"

        for attempt in range(1, max_attempts + 1):
            response = requests.get(url, params={
                "fields": "status_code",
                "access_token": self.access_token,
            }, timeout=15)

            data = response.json()

            if "error" in data:
                raise RuntimeError(
                    f"Instagram status check error: {data['error']['message']}"
                )

            status = data.get("status_code")
            print(f"  Container status (attempt {attempt}): {status}")

            if status == "FINISHED":
                return

            if status == "ERROR":
                raise RuntimeError("Instagram media container processing failed.")

            time.sleep(5)

        raise RuntimeError("Instagram media container did not finish processing in time.")

    def publish_media_container(self, container_id: str) -> str:
        """
        Step 2: Publish the container.
        Returns the Instagram post ID.
        """
        url = f"{self.BASE_URL}/{self.ig_user_id}/media_publish"

        payload = {
            "creation_id": container_id,
            "access_token": self.access_token,
        }

        response = requests.post(url, data=payload, timeout=30)
        data = response.json()

        if "error" in data:
            raise RuntimeError(
                f"Instagram publish error: {data['error']['message']}"
            )

        media_id = data.get("id")

        if not media_id:
            raise RuntimeError("Instagram did not return a media ID after publishing.")

        print(f"  Published successfully. IG Post ID: {media_id}")
        return media_id

    def publish(self, image_url: str, caption: str) -> str:
        """
        Full publish flow:
        1. Create media container
        2. Wait for processing
        3. Publish
        Returns the Instagram post ID.
        """
        container_id = self.create_media_container(image_url, caption)
        self.wait_for_container(container_id)
        return self.publish_media_container(container_id)
