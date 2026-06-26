Victoriaoftheday — Instagram Automation Project

1. Project Overview

Victoriaoftheday is an automated Instagram publishing project.
The project publishes one image per day, each connected to the name Victoria / Vika through language, culture, history, geography, symbolism, mythology, pop culture, or meme-like associations.
Each Instagram post contains:
- one image;
- a short title or caption;
- a very short explanation;
- optional hashtags.
The goal is to create a daily visual series where every post is a small cultural, linguistic, or symbolic discovery around the name Victoria / Vika.
---

2. Core Concept

The name Victoria comes from Latin and means victory.
The project uses this semantic core as the foundation:
Victoria = victory, triumph, beauty, strength, crown, the V sign, cultural memory, history, and unexpected visual associations.The short form Vika can be used more freely through:
- sound associations;
- wordplay;
- visual jokes;
- meme logic;
- phonetic similarity;
- unexpected cultural references.
---

3. Project Stack

The project uses the following stack:
```
Notion
→ GitHub Actions
→ Python script
→ Public image URLs from personal server
→ Instagram Graph API
→ Notion status update

```

Main Components

Component
Purpose
Notion
Content database and editorial calendar
Personal server
Public image hosting
GitHub repository
Source code and project configuration
GitHub Actions
Scheduled daily automation
Python
Publishing logic
Instagram Graph API
Automatic Instagram publishing
Telegram optional
Success/error notifications

---

4. Content Workflow

The content is prepared manually or semi-automatically in advance.
Each post is stored as one row/page in a Notion database.
The Python script runs daily and performs the following workflow:
1. Connect to Notion.
2. Find the post scheduled for today.
3. Check that the post status is Ready.
4. Read the image URL, caption, title, and hashtags.
5. Publish the image to Instagram.
6. Update the Notion status to Posted.
7. Save the Instagram post ID.
8. If an error occurs, update the Notion status to Error.
9. Optionally send a Telegram notification.
---

5. Notion Database Structure

Create a Notion database called:
```
Victoriaoftheday

```
Recommended database properties:
Property
Type
Example
Required
ID


No
Day
Number
1
Yes
Publish Date
Date
2026-01-01
Yes
Title
Text
V-sign
Yes
Category
Select
Victory and Triumph
Yes
Connection Type
Select
Direct/symbolic
No
Caption
Text
The shortest Victoria.
Yes
Hashtags
Text
#Victoria #Vika #365Victorias
No
Image URL
URL
https://example.com/victoria/day001.jpg
Yes
Status
Select
Ready
Yes
IG Post ID
Text
17900000000000000
No
Error
Text
API error message
No
Notes
Text
Internal notes
No

---

6. Recommended Status Values

Use the following values for the Status property:
Status
Meaning
draft
The idea is not ready yet
ready
The post is ready to be published
posted
The post has been published
error
Publication failed
skipped
The post was intentionally skipped
The automation should only publish posts with:
```
Status = ready
Publish Date = today

```

---

7. Image Hosting

Images are stored on a personal server with public access.
Example URL structure:
```
http://www.nadadeneg.com/Votd/day001_v_sign.png
http://www.nadadeneg.com/Votd/day002_laurel_wreath.png
http://www.nadadeneg.com/Votd/day003_trophy.png
```
Recommended image naming pattern:
```
day001.jpg
day002.jpg
day003.jpg
...
day365.jpg

```
Image requirements:
- the URL must be public;
- the URL should use HTTPS;
- the file should be accessible without login;
- the file should return a direct image response;
- the file should not be blocked by hotlink protection;
- the image should be square or Instagram-friendly;
- recommended format: JPG or PNG.
---

8. Instagram Requirements

The project uses the official Instagram publishing flow through the Instagram Graph API.
Required Instagram setup:
1. Instagram Professional account:
	- Business, or
	- Creator.
2. Facebook Page connected to the Instagram account.
3. Meta Developer App.
4. Required access token.
5. Instagram user ID.
The basic publishing flow:
```
1. Create media container
2. Publish media container

```
Conceptually:
```
POST /{ig-user-id}/media
POST /{ig-user-id}/media_publish

```
The Python script sends:
- public image URL;
- caption;
- access token.
---

9. GitHub Repository Structure

Recommended repository structure:
```
365-victorias-publisher/
│
├── .github/
│   └── workflows/
│       └── publish.yml
│
├── src/
│   ├── main.py
│   ├── notion_client.py
│   ├── instagram_client.py
│   ├── telegram_client.py
│   └── config.py
│
├── tests/
│   └── test_caption.py
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── project.md

```

---

10. Environment Variables

Secrets must not be committed to GitHub.
Use GitHub Actions Secrets for production.
Required secrets:
```
NOTION_TOKEN=
NOTION_DATABASE_ID=

IG_USER_ID=
IG_ACCESS_TOKEN=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

```
Optional variables:
```
TIMEZONE=Europe/Vienna
DRY_RUN=false

```

---

11. .env.example

Create a file called .env.example:
```
NOTION_TOKEN=secret_xxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

IG_USER_ID=1234567890
IG_ACCESS_TOKEN=EAAB...

TELEGRAM_BOT_TOKEN=123456:ABCDEF
TELEGRAM_CHAT_ID=123456789

TIMEZONE=Europe/Vienna
DRY_RUN=true

```

---

12. GitHub Actions Workflow

Create this file:
```
.github/workflows/publish.yml

```
Example workflow:
```
name: Publish daily Instagram post

on:
  schedule:
    - cron: "0 8 * * *"
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest

    env:
      NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
      NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
      IG_USER_ID: ${{ secrets.IG_USER_ID }}
      IG_ACCESS_TOKEN: ${{ secrets.IG_ACCESS_TOKEN }}
      TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      TIMEZONE: Europe/Vienna
      DRY_RUN: "false"

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run publisher
        run: python src/main.py

```
Note:
```
GitHub Actions cron runs in UTC.

```
If the desired publishing time is 09:00 Vienna time, adjust the cron time carefully depending on summer/winter time.
For the first MVP, it is acceptable to run the workflow once daily and let the Python script determine the correct date using the configured timezone.
---

13. Python Script Logic

The main script should follow this logic:
```
def main():
    today = get_today_date(timezone="Europe/Vienna")

    post = notion.find_ready_post_by_date(today)

    if not post:
        notify("No ready post found for today.")
        return

    if post["ig_post_id"]:
        notify("Post already published. Skipping.")
        return

    try:
        validate_post(post)

        caption = build_caption(
            title=post["title"],
            caption=post["caption"],
            hashtags=post["hashtags"]
        )

        if DRY_RUN:
            notify(f"DRY RUN: would publish {post['title']}")
            return

        container_id = instagram.create_media_container(
            image_url=post["image_url"],
            caption=caption
        )

        media_id = instagram.publish_media_container(container_id)

        notion.mark_as_posted(
            page_id=post["page_id"],
            ig_post_id=media_id
        )

        notify(f"Posted successfully: {post['title']}")

    except Exception as error:
        notion.mark_as_error(
            page_id=post["page_id"],
            error=str(error)
        )

        notify(f"Publishing error: {post['title']} — {error}")

```

---

14. Caption Format

Recommended Instagram caption format:
```
{Caption}

{Hashtags}

```
Example:
```
The shortest Victoria.

#Victoria #Vika #365Victorias

```
Alternative format:
```
Day {Day}: {Title}

{Caption}

{Hashtags}

```
Example:
```
Day 1: V-sign

The shortest Victoria.

#Victoria #Vika #365Victorias

```

---

15. Validation Rules

Before publishing, the script should validate that:
- Title is not empty;
- Publish Date is today;
- Status is ready;
- Image URL is not empty;
- Image URL starts with https://;
- Caption is not empty;
- IG Post ID is empty;
- image URL returns a successful HTTP response;
- image content type looks like an image;
- the post was not already published.
If validation fails:
```
Status → error
Error → validation error message

```

---

16. Dry Run Mode

The project should support dry-run mode.
When:
```
DRY_RUN=true

```
The script should:
- read the post from Notion;
- validate all fields;
- build the final caption;
- send a test notification;
- not publish anything to Instagram;
- not mark the post as Posted.
This is useful for testing the whole pipeline safely.
---

17. Telegram Notifications

Telegram notifications are optional but recommended.
Send notifications for:
- successful publication;
- missing post for today;
- validation error;
- Instagram API error;
- Notion API error.
Example messages:
```
✅ Posted: Day 1 — V-sign

```

```
⚠️ No ready post found for today.

```

```
❌ Error: Day 12 — Victoria Falls
Image URL is not reachable.

```

---

18. Error Handling

If publication fails, the script should:
1. Catch the exception.
2. Update Notion:
	- Status → error;
	- Error → error message.
3. Send a Telegram notification.
4. Stop execution.
The script should never publish the same post twice.
---

19. Manual Controls

The project should allow manual control through Notion:
Action
How to do it
Prepare post
Set Status to ready
Pause post
Set Status to draft or skipped
Retry failed post
Fix issue and set Status back to ready
Prevent duplicate publishing
Keep IG Post ID filled after publishing
Change schedule
Edit Publish Date

---

20. MVP Scope

The first working version should include:
- Notion database connection;
- query today’s ready post;
- read image URL and caption;
- publish one image post to Instagram;
- update Notion status;
- GitHub Actions scheduled run;
- manual workflow trigger;
- dry-run mode;
- basic Telegram notification.
---

21. Later Improvements

Possible future features:
- automatic image URL checking for all 365 posts;
- weekly recap posts;
- carousel publishing;
- story publishing;
- automatic alt text generation;
- automatic hashtag rotation;
- analytics collection;
- Notion dashboard for post performance;
- Telegram commands:
	- /today
	- /next
	- /status
	- /post_now
	- /pause
- backup Notion database to CSV;
- preview generation before posting;
- AI-assisted caption variations;
- automatic detection of missing images.
---

22. Development Phases


Phase 1 — Setup

- Create GitHub repository.
- Create Notion database.
- Upload several test images to the server.
- Add test rows to Notion.
- Create Meta Developer App.
- Get Instagram access token.
- Add GitHub Secrets.

Phase 2 — Local Python Prototype

- Build Notion client.
- Build Instagram client.
- Build caption builder.
- Test dry-run mode locally.

Phase 3 — GitHub Actions Automation

- Add scheduled workflow.
- Add manual trigger.
- Test workflow with dry-run.
- Test real posting with one test post.

Phase 4 — Production

- Add all 365 posts to Notion.
- Upload all images to the server.
- Set first 30 posts to ready.
- Enable daily scheduled publishing.
- Monitor notifications.

Phase 5 — Optimization

- Add error recovery.
- Add analytics.
- Add weekly summaries.
- Add carousel/story support if needed.
---

23. Security Notes

Do not commit secrets to the repository.
Never store these values directly in code:
- Notion token;
- Instagram access token;
- Telegram bot token;
- database IDs if private;
- account IDs if sensitive.
Use:
```
GitHub Secrets

```
For local development, use:
```
.env

```
The .env file must be included in .gitignore.
---

24. .gitignore

Recommended .gitignore:
```
.env
__pycache__/
*.pyc
.venv/
venv/
.DS_Store
.idea/
.vscode/
logs/

```

---

25. requirements.txt

Initial dependencies:
```
requests
python-dotenv
pytz

```
Optional later:
```
notion-client
pytest

```
For the MVP, plain requests is enough.
---

26. Definition of Done

The MVP is complete when:
- GitHub Actions runs daily;
- the script reads the correct post from Notion;
- the script publishes the image to Instagram;
- the script updates the Notion page to posted;
- the Instagram post ID is saved;
- errors are written back to Notion;
- Telegram notification is sent;
- duplicate publishing is prevented.
---

27. Project Principle

This project should remain simple, reliable, and easy to control manually.
Notion is the source of truth.
Python is the publishing engine.
The personal server is the image host.
GitHub Actions is the scheduler.
Instagram is the output channel.
The automation should never remove editorial control from the creator. It should only remove repetitive manual work.

