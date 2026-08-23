# Victoria of the Day

Every day, one image connected to the name Victoria / Vika — through victory, culture, history, geography, symbols, memes, and linguistic associations.

Automated Instagram publisher for the **Victoria-of-the-day** project.

Follow the project on Instagram: [@kira_starlynne](https://www.instagram.com/kira_starlynne/)

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
3. Builds the caption from `Title` and adds `#VictoriaOfTheDay #Victoria`
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
| `IG_ACCESS_TOKEN` | Yes | Instagram Graph API long-lived access token |
| `IG_TOKEN_EXPIRES_AT` | Yes | Unix timestamp when the Instagram access token expires |
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
| Title | Text (`rich_text`) | Instagram caption text |
| Category | Select | Thematic category |
| Caption | Text | Legacy field; currently not used for publishing |
| Hashtags | Text | Legacy field; currently not used for publishing |
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

**Instagram access token** is a long-lived token that expires after roughly 60 days.

The publisher checks the expiry timestamp on every run. When 14 days or fewer remain, it sends a Telegram warning.

To renew the token:
1. Generate a short-lived User Access Token in Meta Graph API Explorer with the required Instagram permissions.
2. Exchange it for a long-lived token.
3. Verify the new token in Access Token Debugger.
4. Update `IG_ACCESS_TOKEN` in GitHub Secrets.
5. Update `IG_TOKEN_EXPIRES_AT` in GitHub Secrets with the new Unix expiry timestamp.

Token renewal is currently manual; expiry monitoring and Telegram warnings are automatic.

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
| Token expiry monitoring | ✅ Working |
| Token renewal | 🛠️ Manual |
| Carousel publishing | 🔜 Planned |
| Analytics | 🔜 Planned |