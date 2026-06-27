# Victoria of the Day

Every day, one image connected to the name Victoria / Vika — through victory, culture, history, geography, symbols, memes, and linguistic associations.

Automated Instagram publisher for the **Victoria-of-the-day** project.

## Stack

```
Notion → GitHub Actions → Python → Instagram Graph API → Notion update → Telegram
```

| Component | Purpose |
|-----------|---------|
| Notion | Content database and editorial calendar |
| Personal server | Public image hosting |
| GitHub Actions | Daily scheduler (09:00 Vienna time) |
| Python | Publishing logic |
| Instagram Graph API | Automatic Instagram publishing |
| Telegram | Success and error notifications |

---

## How It Works

Every day at 09:00 Vienna time, GitHub Actions runs the Python script which:

1. Connects to Notion and finds today's post where `Status = ready`
2. Validates the image URL
3. Builds the caption from title, text, and hashtags
4. Publishes the image to Instagram
5. Saves the Instagram Post ID back to Notion
6. Sets `Status → posted`
7. Sends a Telegram notification

If anything fails, `Status → error` is written to Notion with the error message, and a ❌ Telegram notification is sent.

---

## Project Structure

```
Victoria-of-the-day/
│
├── .github/
│   └── workflows/
│       └── publish.yml          # Daily scheduled workflow
│
├── src/
│   ├── main.py                  # Main orchestration script
│   ├── notion_client.py         # Notion read and write
│   ├── instagram_client.py      # Instagram Graph API publishing
│   ├── telegram_client.py       # Telegram notifications
│   └── config.py                # Environment variable loader
│
├── requirements.txt
├── .env.example
├── .gitignore
├── project.md
└── README.md
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NOTION_TOKEN` | Yes | Notion integration token |
| `NOTION_DATABASE_ID` | Yes | ID of the Notion database |
| `IG_USER_ID` | Yes | Instagram account numeric ID |
| `IG_ACCESS_TOKEN` | Yes | Instagram Graph API access token |
| `TELEGRAM_BOT_TOKEN` | No | Telegram bot token |
| `TELEGRAM_CHAT_ID` | No | Telegram chat ID for notifications |
| `TIMEZONE` | No | Default: `Europe/Vienna` |
| `DRY_RUN` | No | Default: `true`. Set to `false` to publish |

For local development copy `.env.example` to `.env` and fill in the values.
For production all variables are stored as GitHub Secrets.

---

## Notion Database

The Notion database contains one row per post with these columns:

| Column | Type | Description |
|--------|------|-------------|
| Day | Number | Post number (1–365) |
| Publish Date | Date | Scheduled publish date |
| Title | Text | Short post title |
| Category | Select | Thematic category |
| Caption | Text | Instagram caption text |
| Hashtags | Text | Hashtags |
| Image URL | URL | Public image URL on personal server |
| Status | Select | `draft / ready / posted / error / skipped` |
| IG Post ID | Text | Instagram post ID after publishing |
| Error | Text | Error message if publishing failed |

The automation only publishes posts where `Status = ready` and `Publish Date = today`.

---

## Manual Controls

| Action | How |
|--------|-----|
| Prepare a post | Set `Status → ready` |
| Pause a post | Set `Status → draft` or `skipped` |
| Retry a failed post | Fix the issue, set `Status → ready`, clear `Error` |
| Skip today | Leave no post with `ready` status for today |
| Trigger manually | GitHub Actions → Run workflow |

---

## Telegram Notifications

| Event | Message |
|-------|---------|
| Success | `✅ Posted: Day 1 — V-sign` |
| No post found | `⚠️ No ready post found for 2026-06-27.` |
| Error | `❌ Error: Day 1 — V-sign` + error details |
| Dry run | `🧪 DRY RUN: Day 1 — V-sign` |

---

## Maintenance

**Instagram access token** expires every 60 days. When you receive a ❌ error about an invalid token:
1. Go to [Meta Developer Dashboard](https://developers.facebook.com)
2. Navigate to your app → Instagram → API Setup
3. Generate a new access token
4. Update `IG_ACCESS_TOKEN` in GitHub Secrets

---

## Status

| Feature | Status |
|---------|--------|
| Notion read | ✅ Working |
| Image URL validation | ✅ Working |
| Caption builder | ✅ Working |
| Instagram publishing | ✅ Working |
| Notion write-back | ✅ Working |
| Duplicate publish guard | ✅ Working |
| Dry-run mode | ✅ Working |
| GitHub Actions daily schedule | ✅ Working |
| Telegram notifications | ✅ Working |
| Token refresh automation | 🔜 Planned |
| Carousel publishing | 🔜 Planned |
| Analytics | 🔜 Planned |